# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Migrated from Odoo 16.0 to 18.0
{
    'name': 'ECPay 綠界第三方電子發票模組',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'author': 'ECPAY',
    'website': 'http://www.ecpay.com.tw',
    'license': 'LGPL-3',
    'description': """
        綠界 台灣電子發票Odoo模組\n
        Taiwan E-Invoice integration with ECPay\n
        使用 python3\n
        需要依賴模組: pycryptodome
    """,
    'summary': '電子發票 (Invoice): ECPay 綠界第三方電子發票模組',
    'depends': ['account', 'sale', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'security/ecpay_invoice_groups.xml',
        'views/res_config_setting_view.xml',
        'views/account_invoice_view.xml',
        'views/uniform_invoice_view.xml',
        'views/sale_order_view.xml',
        'views/res_company.xml',
        'wizard/invoice_invalid_wizard.xml',
        'wizard/action_invalid_invoice_wizard.xml',
        'views/menu.xml',
        'data/demo.xml',
        'report/uniform_invoice_report.xml'
    ],
    'external_dependencies': {
        'python': ['pycryptodomex'],
        'bin': [],
    },
    "assets": {
        "web.assets_frontend": [
            "ecpay_invoice_tw/static/src/css/invoice.css",
        ],
    },
    'installable': True,
    'application': True,
}
