# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo.addons.payment.controllers import portal as payment_portal

_logger = logging.getLogger(__name__)


class PaymentPortal(payment_portal.PaymentPortal):
    def _create_transaction(
            self, provider_id, payment_method_id, token_id, amount, currency_id, partner_id, flow,
            tokenization_requested, landing_route, reference_prefix=None, is_validation=False,
            custom_create_values=None, **kwargs
    ):
        """Override of payment to handle ECPay-specific transaction creation.

        Odoo 18 API: Uses provider_id, payment_method_id, token_id instead of payment_option_id.

        :param int provider_id: The provider handling the transaction, as a `payment.provider` id.
        :param int|None payment_method_id: The payment method, as a `payment.method` id.
        :param int|None token_id: The token, if any, as a `payment.token` id.
        :param float|None amount: The amount to pay.
        :param int|None currency_id: The currency, as a `res.currency` id.
        :param int partner_id: The partner making the payment, as a `res.partner` id.
        :param str flow: The payment flow: 'redirect', 'direct' or 'token'.
        :param bool tokenization_requested: Whether tokenization was requested.
        :param str landing_route: The route to redirect after transaction.
        :param str reference_prefix: The custom prefix for the reference.
        :param bool is_validation: Whether this is a validation operation.
        :param dict custom_create_values: Additional create values.
        :return: The sudoed transaction.
        :rtype: payment.transaction
        """
        tx_sudo = super()._create_transaction(
            provider_id=provider_id,
            payment_method_id=payment_method_id,
            token_id=token_id,
            amount=amount,
            currency_id=currency_id,
            partner_id=partner_id,
            flow=flow,
            tokenization_requested=tokenization_requested,
            landing_route=landing_route,
            reference_prefix=reference_prefix,
            is_validation=is_validation,
            custom_create_values=custom_create_values,
            **kwargs
        )

        # Handle ECPay-specific payment type selection
        payment_type = kwargs.get('payment_type')
        if payment_type and tx_sudo.provider_code == 'ECPay':
            tx_sudo.payment_method = payment_type

        return tx_sudo
