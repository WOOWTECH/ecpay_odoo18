# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Migrated from Odoo 16.0 to 18.0

import logging
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ECPayController(http.Controller):
    """Controller for ECPay payment gateway callbacks.

    Handles payment notifications, info notifications (ATM/CVS/BARCODE),
    and customer return from ECPay checkout page.
    """
    _notify_url = "/payment/ecpay/result_notify"
    _return_url = "/payment/ecpay/website_return"
    _info_notify_url = "/payment/ecpay/info_notify"
    _payment_process_url = "/payment/ecpay/website_return"

    @http.route(
        "/payment/ecpay/result_notify",
        type="http",
        methods=["POST"],
        auth="public",
        csrf=False,
    )
    def ecpay_notify(self, **post):
        """Handle ECPay payment result notification (Server POST).

        當消費者付款完成後，綠界會將付款結果參數以 Server POST 回傳到該網址。
        1. 請勿設定與 Client 端接收付款結果網址 OrderResultURL 相同位置，避免程式判斷錯誤。
        2. 請在收到 Server 端付款結果通知後，請正確回應 1|OK 給綠界。

        :return: "1|OK" on success, "0|error" on failure
        """
        _logger.info("ECPay payment notification received: %s", pprint.pformat(post))
        try:
            # Make a copy of post data since ecpay_check_mac_value pops CheckMacValue
            post_data = dict(post)
            # 計算驗證 CheckMacValue 是否相符
            result = request.env["payment.transaction"].sudo().ecpay_check_mac_value(post_data)
            if result:
                # 若為 1 時，代表此交易為模擬付款，請勿出貨。
                # 若為 0 時，代表此交易非模擬付款。
                if post.get("SimulatePaid", "1") == "0" or post.get("RtnCode") == "1" or result == "test":
                    # 執行 odoo 內建交易內容
                    request.env["payment.transaction"].sudo()._handle_notification_data(
                        "ECPay", post
                    )
                    # 執行綠界交易內容(付款結果)
                    request.env["order.ecpay.model"].sudo().order_paid_record(post)
                return "1|OK"
            else:
                _logger.warning("ECPay CheckMacValue verification failed")
                return "0|error"
        except Exception as e:
            _logger.exception("Error processing ECPay notification: %s", e)
            return "0|error"

    @http.route(
        "/payment/ecpay/info_notify",
        type="http",
        methods=["POST"],
        auth="public",
        csrf=False,
    )
    def ecpay_info(self, **post):
        """Handle ECPay payment info notification (ATM/CVS/BARCODE).

        使用 ATM/CVS/BARCODE 付款方式建立訂單完成後，以下參數會以
        Server POST 方式傳送至訂單資料設定的回傳付款網址 [PaymentInfoURL]
        1. 綠界: 以 ServerPost 方式傳送取號結果訊息至特店的 Server 網址 [PaymentInfoURL]
        2. 特店: 收到綠界的取號結果訊息，並判斷檢查碼是否相符
        3. 特店: 檢查碼相符後，於網頁端回應 1|OK

        :return: "1|OK" on success, "0|error" on failure
        """
        _logger.info("ECPay info notification received (ATM/CVS/BARCODE): %s", pprint.pformat(post))
        try:
            # Make a copy of post data since ecpay_check_mac_value pops CheckMacValue
            post_data = dict(post)
            # 計算驗證 CheckMacValue 是否相符
            if request.env["payment.transaction"].sudo().ecpay_check_mac_value(post_data):
                # 執行 odoo 內建交易內容
                request.env["payment.transaction"].sudo()._handle_notification_data(
                    "ECPay", post
                )
                # 執行綠界交易內容(付款資訊)
                request.env["order.ecpay.model"].sudo().order_info_record(post)
                return "1|OK"
            else:
                _logger.warning("ECPay CheckMacValue verification failed for info notify")
                return "0|error"
        except Exception as e:
            _logger.exception("Error processing ECPay info notification: %s", e)
            return "0|error"

    @http.route(
        "/payment/ecpay/website_return",
        type="http",
        methods=["GET", "POST"],
        auth="public",
        csrf=False,
        save_session=False,
    )
    def ecpay_return(self, **post):
        """Handle customer return from ECPay checkout page.

        消費者點選此按鈕後，會將頁面導回到此設定的網址
        導回時不會帶付款結果到此網址，只是將頁面導回而已。
        設定此參數，綠界會在付款完成或取號完成頁面上顯示[返回商店]的按鈕。

        :return: Redirect to payment status page
        """
        _logger.info("ECPay customer return, post data: %s", pprint.pformat(post) if post else "None")
        try:
            if post:
                request.env["payment.transaction"].sudo()._handle_notification_data("ECPay", dict(post))
        except Exception as e:
            _logger.exception("Error processing ECPay return: %s", e)
        return request.redirect("/payment/status")
