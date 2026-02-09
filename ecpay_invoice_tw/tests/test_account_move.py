# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
"""
Unit tests for ECPay Invoice functionality on account.move model.

Tests cover:
- Field writability (BUG-001, BUG-002, BUG-010, BUG-011, BUG-013)
- Carrier number input field
- Lovecode input field
- Validation logic
- Data flow from sale.order to account.move
"""
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestAccountMoveFields(TransactionCase):
    """Test field writability and basic functionality"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a partner for testing
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'test@example.com',
            'street': 'Test Street 123',
        })

    def _create_invoice(self, **kwargs):
        """Helper to create a test invoice"""
        vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'invoice_line_ids': [(0, 0, {
                'name': 'Test Product',
                'quantity': 1,
                'price_unit': 100,
            })],
        }
        vals.update(kwargs)
        return self.env['account.move'].create(vals)

    def test_input_carrier_num_writable(self):
        """BUG-001, BUG-010: input_carrier_num field should accept values"""
        invoice = self._create_invoice()
        invoice.write({'input_carrier_num': '/ABC+123'})
        self.assertEqual(invoice.input_carrier_num, '/ABC+123')

    def test_input_carrier_num_writable_natural_person(self):
        """BUG-001: Natural person carrier number should be writable"""
        invoice = self._create_invoice()
        carrier_num = 'AB12345678901234'  # 16 chars: 2 letters + 14 digits
        invoice.write({'input_carrier_num': carrier_num})
        self.assertEqual(invoice.input_carrier_num, carrier_num)

    def test_is_donation_writable(self):
        """BUG-002, BUG-011: is_donation field should be toggleable"""
        invoice = self._create_invoice()
        invoice.write({'is_donation': True})
        self.assertTrue(invoice.is_donation)
        invoice.write({'is_donation': False})
        self.assertFalse(invoice.is_donation)

    def test_is_print_writable(self):
        """BUG-002, BUG-011: is_print field should be toggleable"""
        invoice = self._create_invoice()
        invoice.write({'is_print': True})
        self.assertTrue(invoice.is_print)
        invoice.write({'is_print': False})
        self.assertFalse(invoice.is_print)

    def test_lovecode_writable(self):
        """BUG-013: lovecode field should accept values"""
        invoice = self._create_invoice()
        invoice.write({'lovecode': '168'})
        self.assertEqual(invoice.lovecode, '168')

    def test_lovecode_7_digits(self):
        """BUG-013: lovecode field should accept 7 digit codes"""
        invoice = self._create_invoice()
        invoice.write({'lovecode': '1234567'})
        self.assertEqual(invoice.lovecode, '1234567')

    def test_ecpay_customer_identifier_writable(self):
        """BUG-013: ecpay_CustomerIdentifier (統編) should be writable"""
        invoice = self._create_invoice()
        invoice.write({'ecpay_CustomerIdentifier': '12345678'})
        self.assertEqual(invoice.ecpay_CustomerIdentifier, '12345678')

    def test_carrier_type_selection(self):
        """carrierType field should accept valid selections"""
        invoice = self._create_invoice()
        # Test all valid carrier types
        for carrier_type in ['1', '2', '3']:
            invoice.write({'carrierType': carrier_type})
            self.assertEqual(invoice.carrierType, carrier_type)

    def test_ec_print_address_writable(self):
        """ec_print_address field should accept values"""
        invoice = self._create_invoice()
        address = '台北市中正區重慶南路一段122號'
        invoice.write({'ec_print_address': address})
        self.assertEqual(invoice.ec_print_address, address)

    def test_ec_ident_name_writable(self):
        """ec_ident_name (發票抬頭) field should accept values"""
        invoice = self._create_invoice()
        invoice.write({'ec_ident_name': 'Test Company Ltd.'})
        self.assertEqual(invoice.ec_ident_name, 'Test Company Ltd.')


class TestAccountMoveOnchange(TransactionCase):
    """Test onchange behaviors"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'test@example.com',
            'street': 'Test Street 123',
        })

    def _create_invoice(self, **kwargs):
        """Helper to create a test invoice"""
        vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
        }
        vals.update(kwargs)
        return self.env['account.move'].create(vals)

    def test_onchange_carrier_type_clears_carrier_num(self):
        """When carrier type is cleared, carrier number should also clear"""
        invoice = self._create_invoice(
            carrierType='3',
            input_carrier_num='/ABC+123'
        )
        # Simulate onchange by calling the method
        invoice.carrierType = False
        invoice._onchange_carrier_type()
        self.assertFalse(invoice.input_carrier_num)

    def test_onchange_carrier_type_to_ecpay_clears_num(self):
        """When carrier type changes to ECPay carrier (1), clear the number"""
        invoice = self._create_invoice(
            carrierType='3',
            input_carrier_num='/ABC+123'
        )
        invoice.carrierType = '1'
        invoice._onchange_carrier_type()
        self.assertFalse(invoice.input_carrier_num)

    def test_onchange_is_print_clears_carrier(self):
        """When is_print is True and carrierType is set, carrier should clear"""
        invoice = self._create_invoice(
            carrierType='3',
            input_carrier_num='/ABC+123'
        )
        invoice.is_print = True
        invoice.set_carrierType_false()
        self.assertFalse(invoice.carrierType)
        self.assertFalse(invoice.input_carrier_num)

    def test_onchange_is_donation_clears_print(self):
        """When is_donation is True, is_print should be cleared"""
        invoice = self._create_invoice(is_print=True)
        invoice.is_donation = True
        invoice.set_is_print_false()
        self.assertFalse(invoice.is_print)


class TestAccountMoveValidation(TransactionCase):
    """Test validation logic for ECPay invoice creation"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'test@example.com',
            'street': 'Test Street 123',
        })

    def _create_invoice(self, **kwargs):
        """Helper to create a test invoice"""
        vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'invoice_line_ids': [(0, 0, {
                'name': 'Test Product',
                'quantity': 1,
                'price_unit': 100,
            })],
        }
        vals.update(kwargs)
        return self.env['account.move'].create(vals)

    def test_validation_print_and_donation_conflict(self):
        """Cannot have both print and donation enabled"""
        invoice = self._create_invoice(
            is_print=True,
            is_donation=True,
        )
        with self.assertRaises(UserError) as context:
            invoice.validate_ecpay_invoice()
        self.assertIn('列印發票與捐贈發票不能同時勾選', str(context.exception))

    def test_validation_print_with_carrier_conflict(self):
        """Cannot have print enabled with carrier type"""
        invoice = self._create_invoice(
            is_print=True,
            carrierType='3',
        )
        with self.assertRaises(UserError) as context:
            invoice.validate_ecpay_invoice()
        self.assertIn('列印發票時，不能夠選擇發票載具', str(context.exception))

    def test_validation_carrier_requires_number(self):
        """Carrier type 2 or 3 requires carrier number"""
        invoice = self._create_invoice(
            carrierType='3',
            input_carrier_num='',
        )
        with self.assertRaises(UserError) as context:
            invoice.validate_ecpay_invoice()
        self.assertIn('請輸入發票載具號碼', str(context.exception))

    def test_validation_requires_address(self):
        """Validation requires customer address"""
        # Create partner without address
        partner_no_addr = self.env['res.partner'].create({
            'name': 'No Address Customer',
            'email': 'test@example.com',
        })
        invoice = self._create_invoice(partner_id=partner_no_addr.id)
        with self.assertRaises(UserError) as context:
            invoice.validate_ecpay_invoice()
        self.assertIn('客戶地址', str(context.exception))

    def test_validation_wrong_move_type(self):
        """Validation should only work for out_invoice"""
        invoice = self._create_invoice()
        # Change move_type to something other than out_invoice
        invoice.move_type = 'out_refund'
        with self.assertRaises(UserError) as context:
            invoice.validate_ecpay_invoice()
        self.assertIn('客戶應收憑單', str(context.exception))


class TestAccountMoveCarrierNumDisplay(TransactionCase):
    """Test carrier number display logic (related field vs input field)"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'test@example.com',
            'street': 'Test Street 123',
        })

    def _create_invoice(self, **kwargs):
        """Helper to create a test invoice"""
        vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
        }
        vals.update(kwargs)
        return self.env['account.move'].create(vals)

    def test_carrier_num_is_related_field(self):
        """carrierNum should be a related field to ecpay_invoice_id"""
        invoice = self._create_invoice()
        # carrierNum is related to ecpay_invoice_id.IIS_Carrier_Num
        # When no ecpay_invoice_id, it should be empty
        self.assertFalse(invoice.carrierNum)

    def test_input_carrier_num_is_independent(self):
        """input_carrier_num should store value independently"""
        invoice = self._create_invoice(input_carrier_num='/TEST123')
        # input_carrier_num stores value directly
        self.assertEqual(invoice.input_carrier_num, '/TEST123')
        # carrierNum (related field) should still be empty
        self.assertFalse(invoice.carrierNum)
