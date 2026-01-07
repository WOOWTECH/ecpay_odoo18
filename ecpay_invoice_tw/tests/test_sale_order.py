# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
"""
Unit tests for ECPay Invoice functionality on sale.order model.

Tests cover:
- Field writability for e-invoice options
- _prepare_invoice data flow to account.move
- Issue #4: Carrier number data flow fix
"""
from odoo.tests.common import TransactionCase


class TestSaleOrderFields(TransactionCase):
    """Test field writability on sale.order"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'test@example.com',
            'street': 'Test Street 123',
        })
        # Create a product for testing
        cls.product = cls.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'type': 'consu',
        })

    def _create_sale_order(self, **kwargs):
        """Helper to create a test sale order"""
        vals = {
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 1,
                'price_unit': 100,
            })],
        }
        vals.update(kwargs)
        return self.env['sale.order'].create(vals)

    def test_ec_print_writable(self):
        """ec_print field should be writable"""
        order = self._create_sale_order()
        order.write({'ec_print': True})
        self.assertTrue(order.ec_print)

    def test_ec_donate_writable(self):
        """ec_donate field should be writable"""
        order = self._create_sale_order()
        order.write({'ec_donate': True})
        self.assertTrue(order.ec_donate)

    def test_ec_donate_number_writable(self):
        """ec_donate_number (lovecode) field should be writable"""
        order = self._create_sale_order()
        order.write({'ec_donate_number': '168'})
        self.assertEqual(order.ec_donate_number, '168')

    def test_ec_carrier_type_writable(self):
        """ec_carrier_type field should accept valid selections"""
        order = self._create_sale_order()
        for carrier_type in ['1', '2', '3']:
            order.write({'ec_carrier_type': carrier_type})
            self.assertEqual(order.ec_carrier_type, carrier_type)

    def test_ec_carrier_number_writable(self):
        """ec_carrier_number field should be writable"""
        order = self._create_sale_order()
        order.write({'ec_carrier_number': '/ABC+123'})
        self.assertEqual(order.ec_carrier_number, '/ABC+123')

    def test_ec_print_address_writable(self):
        """ec_print_address field should be writable"""
        order = self._create_sale_order()
        address = '台北市中正區重慶南路一段122號'
        order.write({'ec_print_address': address})
        self.assertEqual(order.ec_print_address, address)

    def test_ec_ident_name_writable(self):
        """ec_ident_name field should be writable"""
        order = self._create_sale_order()
        order.write({'ec_ident_name': 'Test Company'})
        self.assertEqual(order.ec_ident_name, 'Test Company')

    def test_ec_ident_writable(self):
        """ec_ident (統編) field should be writable"""
        order = self._create_sale_order()
        order.write({'ec_ident': '12345678'})
        self.assertEqual(order.ec_ident, '12345678')


class TestSaleOrderPrepareInvoice(TransactionCase):
    """Test _prepare_invoice method data flow"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'test@example.com',
            'street': 'Test Street 123',
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'type': 'consu',
            'invoice_policy': 'order',  # Important for auto-invoice
        })

    def _create_sale_order(self, **kwargs):
        """Helper to create a test sale order"""
        vals = {
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 1,
                'price_unit': 100,
            })],
        }
        vals.update(kwargs)
        return self.env['sale.order'].create(vals)

    def test_prepare_invoice_includes_carrier_number(self):
        """Issue #4: _prepare_invoice should pass carrier number to input_carrier_num"""
        order = self._create_sale_order(
            ec_carrier_type='3',
            ec_carrier_number='/ABC+123',
        )
        invoice_vals = order._prepare_invoice()
        # Should use input_carrier_num, not carrierNum (which is readonly)
        self.assertEqual(invoice_vals.get('input_carrier_num'), '/ABC+123')
        self.assertEqual(invoice_vals.get('carrierType'), '3')

    def test_prepare_invoice_includes_lovecode(self):
        """_prepare_invoice should pass lovecode correctly"""
        order = self._create_sale_order(
            ec_donate=True,
            ec_donate_number='168',
        )
        invoice_vals = order._prepare_invoice()
        self.assertTrue(invoice_vals.get('is_donation'))
        self.assertEqual(invoice_vals.get('lovecode'), '168')

    def test_prepare_invoice_includes_print_info(self):
        """_prepare_invoice should pass print invoice info"""
        order = self._create_sale_order(
            ec_print=True,
            ec_print_address='Test Address 123',
            ec_ident_name='Test Company',
            ec_ident='12345678',
        )
        invoice_vals = order._prepare_invoice()
        self.assertTrue(invoice_vals.get('is_print'))
        self.assertEqual(invoice_vals.get('ec_print_address'), 'Test Address 123')
        self.assertEqual(invoice_vals.get('ec_ident_name'), 'Test Company')
        self.assertEqual(invoice_vals.get('ecpay_CustomerIdentifier'), '12345678')

    def test_prepare_invoice_natural_person_carrier(self):
        """_prepare_invoice should handle natural person carrier correctly"""
        carrier_num = 'AB12345678901234'  # 16 chars
        order = self._create_sale_order(
            ec_carrier_type='2',
            ec_carrier_number=carrier_num,
        )
        invoice_vals = order._prepare_invoice()
        self.assertEqual(invoice_vals.get('input_carrier_num'), carrier_num)
        self.assertEqual(invoice_vals.get('carrierType'), '2')

    def test_prepare_invoice_no_carrier_type(self):
        """_prepare_invoice should handle no carrier type (ECPay carrier)"""
        order = self._create_sale_order(
            ec_carrier_type='1',
        )
        invoice_vals = order._prepare_invoice()
        self.assertEqual(invoice_vals.get('carrierType'), '1')
        # input_carrier_num should be empty for ECPay carrier type
        self.assertFalse(invoice_vals.get('input_carrier_num'))


class TestSaleOrderToInvoiceFlow(TransactionCase):
    """Test complete flow from sale order to invoice"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'test@example.com',
            'street': 'Test Street 123',
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'type': 'consu',
            'invoice_policy': 'order',
        })

    def _create_sale_order(self, **kwargs):
        """Helper to create a test sale order"""
        vals = {
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 1,
                'price_unit': 100,
            })],
        }
        vals.update(kwargs)
        return self.env['sale.order'].create(vals)

    def test_carrier_number_flows_to_invoice(self):
        """Issue #4: Carrier number should flow from SO to invoice via input_carrier_num"""
        order = self._create_sale_order(
            ec_carrier_type='3',
            ec_carrier_number='/ABC+123',
        )
        # Confirm the order
        order.action_confirm()

        # Create invoice
        invoice = order._create_invoices()

        # Check that carrier number was transferred to input_carrier_num
        self.assertEqual(invoice.input_carrier_num, '/ABC+123')
        self.assertEqual(invoice.carrierType, '3')

    def test_donation_flows_to_invoice(self):
        """Donation info should flow from SO to invoice"""
        order = self._create_sale_order(
            ec_donate=True,
            ec_donate_number='168',
        )
        order.action_confirm()
        invoice = order._create_invoices()

        self.assertTrue(invoice.is_donation)
        self.assertEqual(invoice.lovecode, '168')

    def test_print_info_flows_to_invoice(self):
        """Print invoice info should flow from SO to invoice"""
        order = self._create_sale_order(
            ec_print=True,
            ec_print_address='Test Print Address',
            ec_ident_name='Test Company Name',
            ec_ident='87654321',
        )
        order.action_confirm()
        invoice = order._create_invoices()

        self.assertTrue(invoice.is_print)
        self.assertEqual(invoice.ec_print_address, 'Test Print Address')
        self.assertEqual(invoice.ec_ident_name, 'Test Company Name')
        self.assertEqual(invoice.ecpay_CustomerIdentifier, '87654321')
