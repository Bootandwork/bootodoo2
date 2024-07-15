# invoice_last_payment_date/models/account_move.py
from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    last_payment_date = fields.Date(string='Last Payment Date', readonly=True, compute="_compute_last_payment_date")

    @api.depends('amount_residual_signed')
    def _compute_last_payment_date(self):
        # self.ensure_one()
        for record in self:
            payments = self.env['account.payment'].search([
                ('ref', '=', record.name)
            ], order='date desc', limit=1)
            if payments:
                record.last_payment_date = payments.date
            else:
                payments = self.env['payment.transaction'].search([
                ('invoice_ids', '=', record.id)
            ], order='last_state_change desc', limit=1)
                if payments:
                    record.last_payment_date = payments.last_state_change.date()
                else:
                    record.last_payment_date = False
    # def _compute_last_payment_date(self):
    #     for record in self:
    #         if record.payment_ids:
    #             last_payment = record.payment_ids.sorted(key=lambda p: p.payment_date, reverse=True)[0]
    #             record.last_payment_date = last_payment.payment_date
    #         else:
    #             record.last_payment_date = False


    
        # return payments and payments[0] or False

    # @api.onchange('amount_residual_signed')
    # def _onchange_amount_total(self):
    #     self._compute_last_payment_date()
