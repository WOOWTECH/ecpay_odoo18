# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Migrated from Odoo 16.0 to 18.0

{
    "name": "ECPay 綠界第三方金流模組",
    "category": "Accounting/Payment Providers",
    "summary": "Payment Provider: ECPay 綠界第三方金流模組",
    "version": "18.0.1.0.0",
    "description": """ECPay 綠界第三方金流模組 - Taiwan Payment Gateway Integration""",
    'author': 'ECPAY',
    'website': 'http://www.ecpay.com.tw',
    'license': 'LGPL-3',
    # Removed payment_custom dependency as it may not exist in Odoo 18
    # l10n_tw provides Taiwan localization
    "depends": ["payment", "sale_management", "website_sale"],
    "data": [
        "security/payment_ecpay_access_rule.xml",
        "security/ir.model.access.csv",
        "views/payment_views.xml",
        "views/payment_ecpay_templates.xml",
        "views/payment_ecpay_order_templates.xml",
        "views/payment_ecpay_order_views.xml",
        "views/sale_order.xml",
        "data/payment_provider_data.xml",
        "data/ecpay_credit_limit.xml",
    ],
    "installable": True,
    'application': True,
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
    "assets": {
        'web.assets_frontend': [
            "payment_ecpay/static/src/js/selection.js",
        ],
    },
}
