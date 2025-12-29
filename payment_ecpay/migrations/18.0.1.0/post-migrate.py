# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Ensure ECPay payment method is configured as primary.

    Fixes legacy data from Odoo 16→18 migration where
    primary_payment_method_id might have been incorrectly set.

    In Odoo 18, payment methods with primary_payment_method_id set
    are considered "brand" methods (not primary), and are filtered
    out from checkout by _get_compatible_payment_methods().
    """
    _logger.info("Migrating ECPay payment method to ensure is_primary=True")

    cr.execute("""
        UPDATE payment_method
        SET primary_payment_method_id = NULL
        WHERE code = 'ecpay'
          AND primary_payment_method_id IS NOT NULL
    """)

    affected_rows = cr.rowcount
    if affected_rows:
        _logger.info(f"Fixed {affected_rows} ECPay payment method record(s)")
    else:
        _logger.info("ECPay payment method already correctly configured")
