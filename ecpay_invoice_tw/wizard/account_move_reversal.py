# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Migrated from Odoo 16.0 to 18.0
from odoo import models


class AccountMoveReversalInherit(models.TransientModel):
    _inherit = 'account.move.reversal'

    def reverse_moves(self, **kwargs):
        res = super(AccountMoveReversalInherit, self).reverse_moves(**kwargs)
        context = dict(self._context or {})
        # 取得欲作廢或折讓的應收憑單
        invoices = self.env['account.move'].browse(context.get('active_ids'))
        # TODO 使用search 會導致全部的reversed_entry_id = invoice.id 都會被影響，應該從res 來檢查被創建的reversed moves
        res_id = res.get('res_id', False)
        if res_id:
            reversed_ids = [res_id]
        else:
            reversed_ids = res.get('domain')[0][2]
        out_refunds = self.env['account.move'].browse(reversed_ids)
        for invoice in invoices:
            # 如果沒有產生電子發票則不需做關於電子發票相關動作
            if not invoice.ecpay_invoice_id:
                continue

            reversed_moves = out_refunds.filtered(lambda r: r.reversed_entry_id.id == invoice.id)
            if not reversed_moves:
                continue
            #  流程改變 折讓就是折讓 與作廢無關
            # Odoo 18: refund_method removed, use is_modify parameter instead
            if kwargs.get('is_modify', False):
                # 設定該折讓單要關聯折讓的統一發票
                reversed_moves.write({
                    'ecpay_invoice_id': invoice.ecpay_invoice_id.id,
                    'is_refund': True
                })
                for move in reversed_moves:
                    # move.run_invoice_invalid()
                    move.run_refund()
            else:
                reversed_moves.write({
                    'ecpay_invoice_id': invoice.ecpay_invoice_id.id,
                    'is_refund': True
                })
            invoice.uniform_state = 'invalid'

        return res
