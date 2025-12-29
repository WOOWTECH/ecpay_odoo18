# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Migrated to Odoo 18.0 - hook signatures changed from (cr, registry) to (env)
from . import sdk
from . import models
from . import controllers

from odoo.addons.payment import setup_provider, reset_payment_provider


def post_init_hook(env):
    """Odoo 18 post_init_hook takes env parameter"""
    setup_provider(env, 'ECPay')


def uninstall_hook(env):
    """Odoo 18 uninstall_hook takes env parameter"""
    reset_payment_provider(env, "ECPay")
