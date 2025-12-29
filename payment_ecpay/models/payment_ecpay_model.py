# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Migrated from Odoo 16.0 to 18.0

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


# 20230525 16 新增  信用卡分期期數 3 6 12 18 24
class ECPayCreditLimit(models.Model):
    _name = 'ecpay.credit.limit'
    _description = 'ECPay 信用卡分期期數'

    name = fields.Char(string='期數')

    # Odoo 18: name_get is deprecated, use display_name compute instead
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name or ''


# 20220105 15 版新增


class AccountPaymentMethod(models.Model):
    _inherit = "account.payment.method"

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res["ECPay"] = {"mode": "unique", "domain": [("type", "=", "bank")]}
        return res


# 20220108 15 版修改
class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(
        selection_add=[("ECPay", "ECPay 綠界第三方支付")], ondelete={"ECPay": "set default"}
    )

    MerchantID = fields.Char(
        string="特店編號", required_if_provider="ECPay", groups="base.group_user", help="特店編號"
    )
    HashKey = fields.Char(
        string="介接 HashKey", groups="base.group_user", required_if_provider="ECPay"
    )
    HashIV = fields.Char(
        string="介接 HashIV", groups="base.group_user", required_if_provider="ECPay"
    )

    ecpay_credit = fields.Boolean(
        string="信用卡一次付清", default=True, help="信用卡一次付清", groups="base.group_user"
    )
    # Odoo Ecpay 信用卡分期
    ecpay_credit_ids = fields.Many2many('ecpay.credit.limit', string='信用卡分期期數')
    # Odoo 金流測試報告 20181228
    ecpay_apple_pay = fields.Boolean(
        string="Apple Pay",
        default=True,
        help="Apple Pay (若為 PC 版時不支援)",
        groups="base.group_user",
    )
    ecpay_webatm = fields.Boolean(
        string="網路 ATM", default=True, help="網路 ATM (若為手機版時不支援)", groups="base.group_user"
    )
    ecpay_atm = fields.Boolean(
        string="自動櫃員機 ATM", default=True, help="自動櫃員機 ATM", groups="base.group_user"
    )
    ecpay_atm_expiredate = fields.Integer(string='ATM 繳費限制天數', default=3,
                                          help="若需設定最長 60 天，最短1天。未設定此參數則預設為3天",
                                          groups="base.group_user")
    ecpay_cvs = fields.Boolean(
        string="超商代碼", default=True, help="超商代碼", groups="base.group_user"
    )
    ecpay_cvs_expiredate = fields.Integer(string='超商代碼繳費限制天數', default=7,
                                          help="預設為10080分鐘, 等同 7 天。帶入數值不可超過43200分鐘, 也就是 30 天。",
                                          groups="base.group_user")
    ecpay_barcode = fields.Boolean(
        string="超商條碼", default=True, help="超商條碼 (若為手機版時不支援)", groups="base.group_user"
    )
    ecpay_barcode_expiredate = fields.Integer(string='超商條碼繳費限制天數', default=7,
                                              help="若未設定此參數，預設為7天。若需設定最長 30 天，最短1天。",
                                              groups="base.group_user")
    ecpay_bnpl_pay = fields.Boolean(string='無卡分期BNPL', default=True, help="無卡分期BNPL", groups="base.group_user")
    ecpay_twqr_pay = fields.Boolean(string='行動支付TWQR', default=True, help="行動支付TWQR", groups="base.group_user")
    ecpay_domain = fields.Char(
        string="網域名稱",
        default="https://your_domain_name/",
        groups="base.group_user",
        required_if_provider="ecpay",
    )

    def _ecpay_get_api_url(self):
        """Return the ECPay API URL based on provider state."""
        self.ensure_one()
        if self.state == "enabled":
            return "https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5"
        else:
            return "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"

    def _get_default_payment_method_codes(self):
        """Override of `payment` to return the default payment method codes.

        Note: self.ensure_one()

        :return: The default payment method codes.
        :rtype: set
        """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'ECPay':
            return default_codes
        return {'ecpay'}

    def _get_redirect_form_view(self, is_validation=False):
        """Override of `payment` to return the ECPay redirect form view.

        Note: self.ensure_one()

        :param bool is_validation: Whether the operation is a validation.
        :return: The view of the redirect form template.
        :rtype: ir.ui.view record
        """
        self.ensure_one()
        if self.code != "ECPay":
            return super()._get_redirect_form_view(is_validation=is_validation)
        return self.env.ref("payment_ecpay.redirect_form")

    @api.model
    def _get_compatible_providers(self, *args, currency_id=None, **kwargs):
        """Override of `payment` to filter ECPay provider based on delivery method.

        :return: The compatible providers.
        :rtype: payment.provider recordset
        """
        providers = super()._get_compatible_providers(*args, currency_id=currency_id, **kwargs)
        sale_order_id = kwargs.get('sale_order_id')

        if not sale_order_id:
            return providers

        sale_order = self.env['sale.order'].browse(sale_order_id)

        # 當有安裝 delivery (送貨/交貨) 模組，才會有 carrier_id 的欄位
        # Check if delivery module is installed and carrier has IsCollection
        if hasattr(sale_order, 'carrier_id') and sale_order.carrier_id:
            if hasattr(sale_order.carrier_id, 'IsCollection') and sale_order.carrier_id.IsCollection:
                if hasattr(sale_order.carrier_id, 'payment_provider_id'):
                    return providers.filtered(lambda p: p.id == sale_order.carrier_id.payment_provider_id.id)

        return providers
