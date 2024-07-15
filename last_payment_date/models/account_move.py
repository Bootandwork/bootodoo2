# invoice_last_payment_date/models/account_move.py
from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    last_payment_date = fields.Date(string='Last Payment Date', readonly=True, compute="_compute_last_payment_date")

    @api.depends('amount_residual_signed')
    def _compute_last_payment_date(self):
        self.ensure_one()
        payments = self.env['payment.transaction'].search([
            ('invoice_ids', 'in', self.id)
        ], order='last_state_change desc', limit=1)
        for record in self:
            if payments:
                record.last_payment_date = payments
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
