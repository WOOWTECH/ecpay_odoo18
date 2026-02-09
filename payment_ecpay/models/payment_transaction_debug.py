# -*- coding: utf-8 -*-
# ==============================================================================
# Payment Transaction Debug Logging for ECPay Migration
# ==============================================================================
#
# This module adds comprehensive debug logging to track the payment transaction
# flow in Odoo 18 to diagnose auto-invoice issues.
#
# To enable: Add DEBUG_PAYMENT_FLOW=1 to environment or odoo.conf
# ==============================================================================

import traceback
import logging
import os
from functools import wraps

from odoo import models, api, fields

_logger = logging.getLogger(__name__)

# Check if debug mode is enabled
DEBUG_ENABLED = os.environ.get('DEBUG_PAYMENT_FLOW', '0') == '1'


def get_safe_record_info(record):
    """
    Extract debug information safely from any Odoo model.

    Uses Odoo's field introspection to avoid AttributeError when accessing
    fields that don't exist on the model.

    Architecture pattern: Safe field access with model introspection
    """
    info = {
        '_model': record._name,
        'id': record.id,
    }

    # Safely add common fields if they exist
    field_names = record._fields.keys()

    if 'name' in field_names:
        info['name'] = record.name
    if 'reference' in field_names:
        info['reference'] = record.reference
    if 'state' in field_names:
        info['state'] = record.state

    # payment.transaction specific fields
    if 'is_post_processed' in field_names:
        info['is_post_processed'] = record.is_post_processed
    if 'sale_order_ids' in field_names:
        info['sale_orders'] = record.sale_order_ids.mapped('name')
        info['sale_order_states'] = record.sale_order_ids.mapped('state')
    if 'operation' in field_names:
        info['operation'] = record.operation

    # sale.order specific fields
    if 'invoice_status' in field_names:
        info['invoice_status'] = record.invoice_status
    if 'amount_total' in field_names:
        info['amount_total'] = record.amount_total

    # account.move specific fields
    if 'move_type' in field_names:
        info['move_type'] = record.move_type
    if 'payment_state' in field_names:
        info['payment_state'] = record.payment_state

    return info


def debug_log(method_name):
    """
    Decorator to add debug logging to any Odoo model method.

    Architecture improvements:
    - Model-agnostic: Works with any Odoo model (payment.transaction, sale.order, account.move)
    - Safe field access: Uses _fields introspection to avoid AttributeError
    - Structured logging: Provides context, call stack, and execution flow

    Usage:
        @debug_log('method_name')
        def method_name(self):
            return super().method_name()
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not DEBUG_ENABLED:
                return func(self, *args, **kwargs)

            # Use generic 'record' instead of 'tx' to avoid misleading variable names
            record_info = []
            for record in self:
                record_info.append(get_safe_record_info(record))

            _logger.info(
                "\n" + "=" * 80 +
                "\n[ECPAY-DEBUG] %s() ENTER" +
                "\n" + "-" * 80 +
                "\nModel: %s" +
                "\nRecords: %s" +
                "\nArgs: %s" +
                "\nKwargs: %s" +
                "\nContext keys: %s" +
                "\nCall stack (last 6 frames):\n%s" +
                "\n" + "=" * 80,
                method_name,
                self._name,
                record_info,
                args,
                kwargs,
                list(self.env.context.keys()),
                ''.join(traceback.format_stack()[-7:-1])
            )

            try:
                result = func(self, *args, **kwargs)

                # Log result - safely handle different return types
                result_info = []
                if hasattr(result, '_name') and hasattr(result, 'ids'):
                    # Result is an Odoo recordset
                    for record in result:
                        result_info.append(get_safe_record_info(record))

                _logger.info(
                    "\n[ECPAY-DEBUG] %s() EXIT SUCCESS" +
                    "\nResult type: %s" +
                    "\nResult: %s" +
                    "\n" + "-" * 80,
                    method_name,
                    type(result).__name__,
                    result_info if result_info else result
                )
                return result

            except Exception as e:
                _logger.error(
                    "\n[ECPAY-DEBUG] %s() EXIT WITH EXCEPTION" +
                    "\nException: %s: %s" +
                    "\nTraceback:\n%s" +
                    "\n" + "-" * 80,
                    method_name,
                    type(e).__name__,
                    str(e),
                    traceback.format_exc()
                )
                raise

        return wrapper
    return decorator


class PaymentTransactionDebug(models.Model):
    """Debug logging overrides for payment.transaction."""

    _inherit = 'payment.transaction'

    @debug_log('_set_pending')
    def _set_pending(self, state_message=None, extra_allowed_states=()):
        return super()._set_pending(state_message, extra_allowed_states)

    @debug_log('_set_authorized')
    def _set_authorized(self, state_message=None, extra_allowed_states=()):
        return super()._set_authorized(state_message, extra_allowed_states)

    @debug_log('_set_done')
    def _set_done(self, state_message=None, extra_allowed_states=()):
        return super()._set_done(state_message, extra_allowed_states)

    @debug_log('_set_canceled')
    def _set_canceled(self, state_message=None, extra_allowed_states=()):
        return super()._set_canceled(state_message, extra_allowed_states)

    @debug_log('_set_error')
    def _set_error(self, state_message, extra_allowed_states=()):
        return super()._set_error(state_message, extra_allowed_states)

    @debug_log('_post_process')
    def _post_process(self):
        if DEBUG_ENABLED:
            # Log auto_invoice setting
            auto_invoice = self.env['ir.config_parameter'].sudo().get_param('sale.automatic_invoice')
            _logger.info(
                "[ECPAY-DEBUG] _post_process() auto_invoice setting: %s",
                auto_invoice
            )
        return super()._post_process()

    @debug_log('_check_amount_and_confirm_order')
    def _check_amount_and_confirm_order(self):
        return super()._check_amount_and_confirm_order()

    @debug_log('_invoice_sale_orders')
    def _invoice_sale_orders(self):
        if DEBUG_ENABLED:
            for tx in self:
                _logger.info(
                    "[ECPAY-DEBUG] _invoice_sale_orders() for tx %s" +
                    "\n  Sale orders: %s" +
                    "\n  Order states: %s" +
                    "\n  Order invoice_status: %s",
                    tx.reference,
                    tx.sale_order_ids.mapped('name'),
                    tx.sale_order_ids.mapped('state'),
                    tx.sale_order_ids.mapped('invoice_status')
                )
        return super()._invoice_sale_orders()


class AccountMoveDebug(models.Model):
    """Debug logging overrides for account.move (invoice)."""

    _inherit = 'account.move'

    @debug_log('action_post')
    def action_post(self):
        if DEBUG_ENABLED:
            for move in self:
                _logger.info(
                    "[ECPAY-DEBUG] action_post() for invoice %s" +
                    "\n  Move type: %s" +
                    "\n  State: %s" +
                    "\n  Company auto_invoice: %s" +
                    "\n  uniform_state: %s" +
                    "\n  ecpay_invoice_id: %s",
                    move.name,
                    move.move_type,
                    move.state,
                    getattr(move.company_id, 'auto_invoice', 'N/A'),
                    getattr(move, 'uniform_state', 'N/A'),
                    getattr(move, 'ecpay_invoice_id', 'N/A')
                )
        return super().action_post()


class SaleOrderDebug(models.Model):
    """Debug logging overrides for sale.order."""

    _inherit = 'sale.order'

    @debug_log('action_confirm')
    def action_confirm(self):
        return super().action_confirm()

    @debug_log('_create_invoices')
    def _create_invoices(self, grouped=False, final=False, date=None):
        if DEBUG_ENABLED:
            for order in self:
                _logger.info(
                    "[ECPAY-DEBUG] _create_invoices() for order %s" +
                    "\n  State: %s" +
                    "\n  Invoice status: %s" +
                    "\n  Amount total: %s" +
                    "\n  grouped=%s, final=%s, date=%s",
                    order.name,
                    order.state,
                    order.invoice_status,
                    order.amount_total,
                    grouped, final, date
                )
        return super()._create_invoices(grouped, final, date)
