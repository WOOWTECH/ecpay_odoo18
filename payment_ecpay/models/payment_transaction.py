# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Migrated from Odoo 16.0 to 18.0

import logging
import pprint
from datetime import datetime, timedelta

from werkzeug import urls

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from odoo.addons.payment_ecpay.controllers.main import ECPayController
from odoo.addons.payment_ecpay.sdk.ecpay_payment_sdk import ECPayPaymentSdk

_logger = logging.getLogger(__name__)


# 20220108 15 版修改、20230524 修改For V16 方法及欄位對應
class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    payment_method = fields.Char(string='付款方式選擇', readonly=True, copy=False)

    def _get_specific_processing_values(self, processing_values):
        """Override to return ECPay-specific processing values."""
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != 'ECPay':
            return res
        if self.invoice_ids:
            # 20220108 15 版修改
            res['reference'] = self.invoice_ids[0].display_name
            self.reference = self.invoice_ids[0].display_name
        return res

    def _get_specific_rendering_values(self, processing_values):
        """Override to return ECPay rendering values for the payment form."""
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != "ECPay":
            return res

        ChoosePayment = self.payment_method or 'ALL'
        CreditInstallment = ''
        payment_method_check = ['ATM', 'CVS', 'BARCODE']

        # Handle credit card installment selection
        if self.payment_method == "ecpay_credit_ids":
            for rec in self.provider_id.ecpay_credit_ids:
                CreditInstallment += rec.name + ','
            ChoosePayment = 'Credit'

        base_url = self.provider_id.get_base_url()

        sale_order_name = processing_values["reference"].split("-", 1)[0]

        # 取得 ECPay 的後台設定值
        ecpay_payment_sdk = self._ecpay_get_sdk()

        # 取得 domain - ECPay requires HTTPS
        base_url = base_url.replace("http:", "https:", 1)

        # 組合商品名稱
        item_name = ""
        rendering_values = dict()
        sale_order = (
            self.env["sale.order"].sudo().search([("name", "=", sale_order_name)], limit=1)
        )
        # 如果商品名稱有多筆，需在金流選擇頁一行一行顯示商品名稱的話，商品名稱請以符號 # 分隔
        if sale_order:
            for sale_order_line in sale_order.order_line:
                sep = "\n"
                sale_order_line_name = sale_order_line.name.split(sep, 1)[0]
                item_name += sale_order_line_name + "#"
            item_name = item_name.strip("#")

        # 建立綠界需要的交易資料, 需連動到 payment_ecpay_templates.xml
        params = {
            "MerchantTradeNo": f'odooN{(datetime.now() + timedelta(hours=8)).strftime("%m%d%H%M%S")}',
            "MerchantTradeDate": (datetime.now() + timedelta(hours=8)).strftime("%Y/%m/%d %H:%M:%S"),
            "TotalAmount": int(processing_values["amount"]),
            "TradeDesc": "ecpay_module_odoo18",
            "ItemName": item_name if item_name else "商品一批",
            "ReturnURL": urls.url_join(base_url, ECPayController._notify_url),
            "ClientBackURL": urls.url_join(base_url, ECPayController._return_url),
            "OrderResultURL": urls.url_join(base_url, ECPayController._return_url),
            "PaymentInfoURL": urls.url_join(base_url, ECPayController._info_notify_url),
            "ChoosePayment": ChoosePayment,
            "CreditInstallment": CreditInstallment[:-1] if CreditInstallment else '',
            "NeedExtraPaidInfo": "Y",
            "CustomField1": processing_values["reference"],
        }

        # Set expiration dates based on payment method
        if ChoosePayment in payment_method_check:
            if ChoosePayment == 'ATM':
                # ATM: 天數
                params['ExpireDate'] = self.provider_id.ecpay_atm_expiredate
            elif ChoosePayment == 'CVS':
                # CVS: 傳送分鐘數，須將天數轉換為分鐘數
                params['StoreExpireDate'] = self.provider_id.ecpay_cvs_expiredate * 24 * 60
            else:
                # Barcode: 傳送分鐘數
                params['StoreExpireDate'] = self.provider_id.ecpay_barcode_expiredate * 24 * 60

        # 準備將 form 資料傳給 template redirect_form,
        # 讓 redirect_form 自動 submit 出去 post 給綠界
        rendering_values["parameters"] = ecpay_payment_sdk.create_order(params)
        rendering_values["api_url"] = self.provider_id._ecpay_get_api_url()

        _logger.info("ECPay rendering values for transaction %s: api_url=%s",
                     self.reference, rendering_values["api_url"])

        return rendering_values

    @api.model
    def _get_tx_from_notification_data(self, provider, data):
        """Find the transaction from ECPay callback data using CustomField1 reference."""
        tx = super()._get_tx_from_notification_data(provider, data)
        if provider != "ECPay":
            return tx
        # 透過 reference 去找系統有沒有這筆訂單
        reference = data.get("CustomField1")
        if not reference:
            error_msg = (
                    _("ECPay: received data with missing reference (%s)") % reference
            )
            _logger.info(error_msg)
            raise ValidationError(error_msg)

        tx = self.search([("reference", "=", reference)])
        if not tx or len(tx) > 1:
            error_msg = "ECPay: received data for reference %s" % (
                pprint.pformat(reference)
            )
            if not tx:
                error_msg += "; no order found"
            else:
                error_msg += "; multiple order found"
            _logger.info(error_msg)
            raise ValidationError(error_msg)

        _logger.info(tx)
        return tx

    def _process_notification_data(self, data):
        """Process ECPay callback: set transaction to done/pending/error based on RtnCode."""
        super()._process_notification_data(data)
        if self.provider_code != "ECPay":
            return

        return_code = int(data.get("RtnCode"))
        payment_type = data.get("PaymentType")
        res = {
            "acquirer_reference": data.get("CustomField1"),
            "state_message": data.get("RtnMsg"),
        }
        self.provider_reference = res["acquirer_reference"]
        # 若回傳值為 1 時，為付款成功
        if return_code == 1:
            self._set_done()
        # ATM 回傳值時為 2 時，交易狀態為取號成功
        # CVS/BARCODE 回傳值時為 10100073 時，交易狀態為取號成功
        elif (
                (("ATM" in payment_type) and (return_code == 2))
                or (("BARCODE" in payment_type) and (return_code == 10100073))
                or (("CVS" in payment_type) and (return_code == 10100073))
                or (("BNPL_URICH" in payment_type))
        ):
            pending = "Received notification for payment %s: %s" % (
                res["acquirer_reference"],
                res["state_message"],
            )
            self._set_pending(state_message=pending)
        else:
            error = "Received unrecognized status for ECPay payment %s: %s" % (
                res["acquirer_reference"],
                res["state_message"],
            )
            self._set_error(state_message=error)

    @api.model
    def _ecpay_get_sdk(self):
        # 取得 ECPay 的後台設定值
        ecpay_setting = self.env["payment.provider"].search(
            [("code", "=", "ECPay")], limit=1
        )
        return ECPayPaymentSdk(
            MerchantID=ecpay_setting.MerchantID,
            HashKey=ecpay_setting.HashKey,
            HashIV=ecpay_setting.HashIV,
        )

    def _post_process(self):
        """Override to warn about misconfigured products. See ISSUE-002."""
        res = super()._post_process()

        # ISSUE-002: Warn if products with invoice_policy='delivery' are auto-invoiced
        for tx in self.filtered(
            lambda t: t.provider_code == 'ECPay' and t.state == 'done' and t.sale_order_ids
        ):
            for order in tx.sale_order_ids.filtered(lambda so: so.state == 'sale'):
                for line in order.order_line.filtered(
                    lambda l: l.product_id.invoice_policy == 'delivery'
                    and l.qty_to_invoice < 0
                ):
                    _logger.warning(
                        "ISSUE-002: Product '%s' has invoice_policy='delivery' causing "
                        "invoice_status bug. Change to 'order'. Order: %s",
                        line.product_id.name, order.name
                    )

        return res

    @api.model
    def ecpay_check_mac_value(self, post):
        # 取得 ECPay 的 SDK
        ecpay_payment_sdk = self._ecpay_get_sdk()
        # 先將 CheckMacValue 取出
        CheckMacValue = post.pop("CheckMacValue")
        # 將 POST data 計算驗證是否相符
        if CheckMacValue == ecpay_payment_sdk.generate_check_value(post):
            s = self.search([("reference", "=", post.get("CustomField1", ""))], limit=1)
            return s.provider_id.state if any(s) else ""
        else:
            error_msg = _("Ecpay: CheckMacValue is not correct")
            _logger.info(error_msg)
            return False
