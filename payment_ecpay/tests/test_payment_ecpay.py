# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestPaymentEcpay(TransactionCase):
    """Test cases for ECPay payment module."""

    def test_payment_method_is_primary(self):
        """Verify ECPay payment method is configured as primary.

        In Odoo 18, only primary payment methods (is_primary=True)
        are shown at checkout. This test ensures ECPay is correctly
        configured as a primary method.
        """
        method = self.env.ref('payment_ecpay.payment_method_ecpay')
        self.assertTrue(
            method.is_primary,
            "ECPay payment method must be primary (primary_payment_method_id should be False)"
        )
        self.assertFalse(
            method.primary_payment_method_id,
            "ECPay should not have a parent payment method"
        )

    def test_payment_provider_exists(self):
        """Verify ECPay payment provider is created."""
        provider = self.env.ref('payment_ecpay.payment_provider_ecpay')
        self.assertTrue(provider.exists(), "ECPay provider should exist")
        self.assertEqual(provider.code, 'ECPay', "Provider code should be 'ECPay'")

    def test_payment_method_linked_to_provider(self):
        """Verify ECPay payment method is linked to provider."""
        provider = self.env.ref('payment_ecpay.payment_provider_ecpay')
        method = self.env.ref('payment_ecpay.payment_method_ecpay')

        self.assertIn(
            method.id,
            provider.payment_method_ids.ids,
            "ECPay payment method should be linked to ECPay provider"
        )
        self.assertIn(
            provider.id,
            method.provider_ids.ids,
            "ECPay provider should be linked to ECPay payment method"
        )

    def test_payment_method_active(self):
        """Verify ECPay payment method is active."""
        method = self.env.ref('payment_ecpay.payment_method_ecpay')
        self.assertTrue(method.active, "ECPay payment method should be active")
