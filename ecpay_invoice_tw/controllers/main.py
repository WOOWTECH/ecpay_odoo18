# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Migrated from Odoo 16.0 to 18.0
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class EcpayInvoiceController(http.Controller):

    @http.route('/payment/ecpay/save_invoice_type', type='json', methods=['POST'], auth="public")
    def save_invoice_type(self, **kwargs):
        """Save e-invoice type selection to sale order.

        Accepts parameters from both old (Odoo 16) and new (Odoo 18) JavaScript:
        - Old: invoiceType, e_type
        - New: print_flag, donate_flag, invoice_type
        """
        try:
            order_id = request.session.get('sale_order_id')
            if not order_id:
                _logger.warning('ECPay: No sale_order_id in session')
                return '200'  # No order to update, but not an error

            order = request.env['sale.order'].sudo().browse(order_id)
            if not order.exists():
                _logger.warning(f'ECPay: Order {order_id} not found')
                return '200'

            _logger.info(f'ECPay: Saving invoice data for order {order.name}, kwargs: {kwargs}')

            res = {
                'ec_ident_name': '',
                'ec_ident': '',
                'ec_print': False,
                'ec_donate': False,
                'ec_donate_number': '',
                'ec_carrier_type': False,
                'ec_carrier_number': '',
            }

            # Case 1: Print invoice (new JS uses print_flag)
            if kwargs.get('print_flag'):
                if kwargs.get('ident_flag'):
                    res['ec_ident_name'] = kwargs.get('identifier_name', '')
                    res['ec_ident'] = kwargs.get('identifier', '')
                res['ec_print_address'] = kwargs.get('invoice_address', '')
                res['ec_print'] = True
            # Case 2: Donate invoice (new JS uses donate_flag)
            elif kwargs.get('donate_flag'):
                res['ec_donate'] = True
                res['ec_donate_number'] = kwargs.get('LoveCode', '')
            # Case 3: Electronic invoice with carrier (default case)
            else:
                # Support both old (e_type) and new (invoice_type) parameter names
                invoice_type = kwargs.get('invoice_type', kwargs.get('e_type', 0))
                # Convert to string for comparison (JS may send int or string)
                invoice_type_str = str(invoice_type) if invoice_type else '0'

                if invoice_type_str == '0':
                    res['ec_carrier_type'] = False
                else:
                    res['ec_carrier_type'] = invoice_type_str

                if invoice_type_str in ('2', '3'):
                    res['ec_carrier_number'] = kwargs.get('CarrierNum', '')
                else:
                    res['ec_carrier_number'] = ''

            _logger.info(f'ECPay: Writing to order {order.name}: {res}')
            order.write(res)
            _logger.info(f'ECPay: Successfully updated order {order.name}')

            return '200'
        except Exception as e:
            _logger.exception(f'ECPay: Error saving invoice type: {e}')
            return '200'  # Return success to not block payment, but log the error
