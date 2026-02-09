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

            # Case 1: Print invoice
            if kwargs.get('print_flag'):
                # Case 2: Print invoice with unified business number
                if kwargs.get('ident_flag'):
                    res['ec_ident_name'] = kwargs.get('identifier_name', '')
                    res['ec_ident'] = kwargs.get('identifier', '')
                res['ec_print_address'] = kwargs.get('invoice_address', '')
                res['ec_print'] = True
            # Case 3: Donate invoice
            elif kwargs.get('donate_flag'):
                res['ec_donate'] = True
                res['ec_donate_number'] = kwargs.get('LoveCode', '')
            # Case 4: Electronic invoice with carrier (no print, no donate)
            else:
                # Convert to string for comparison (JS may send int or string)
                invoice_type = str(kwargs.get('invoice_type', '0'))
                if invoice_type == '0':
                    res['ec_carrier_type'] = False
                else:
                    res['ec_carrier_type'] = invoice_type

                if invoice_type in ('2', '3'):
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
