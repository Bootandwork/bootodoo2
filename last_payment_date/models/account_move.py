# invoice_last_payment_date/models/account_move.py
from odoo import models, fields, api
from openerp.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    last_payment_date = fields.Date(string='Last Payment Date', readonly=True, compute="_compute_last_payment_date")

    @api.depends('amount_residual_signed')
    def _compute_last_payment_date(self):
        for record in self:
            if record.payment_state != "not_paid":
                # Search for the latest payment date from account.payment
                payments = self.env['account.payment'].search([
                    ('ref', '=', record.name)
                ], order='date desc')
                
                # Search for the latest payment date from payment.transaction
                transactions = self.env['payment.transaction'].search([
                    ('invoice_ids', 'in', record.ids)
                ], order='last_state_change desc')
                
                # Search for the latest payment date from account.move.line
                all_payments = self.env['account.move.line'].search([
                    ('name', '=', record.name)
                ], limit=1)
                
                if all_payments:
                    move_lines = self.env['account.move.line'].search([
                        ('matching_number', '=', all_payments.matching_number)
                    ], order='date desc')
                else:
                    move_lines = self.env['account.move.line'].browse()

                # Collect the latest date from each type
                payment_dates = [p.date for p in payments] + \
                                [t.last_state_change for t in transactions] + \
                                [m.date for m in move_lines]
                
                if payment_dates:
                    # Assign the most recent date
                    record.last_payment_date = max(payment_dates)
                else:
                    record.last_payment_date = False
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
