# invoice_last_payment_date/models/account_move.py
from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    last_payment_date = fields.Date(string='Last Payment Date', readonly=True)

    @api.depends('amount_residual_signed')
    def _compute_last_payment_date(self):
        for record in self:
            if record.payment_ids:
                last_payment = record.payment_ids.sorted(key=lambda p: p.payment_date, reverse=True)[0]
                record.last_payment_date = last_payment.payment_date
            else:
                record.last_payment_date = False

    @api.onchange('amount_residual_signed')
    def _onchange_amount_total(self):
        self._compute_last_payment_date()
