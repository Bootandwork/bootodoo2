from odoo import models, fields, api
from openerp.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    last_payment_date = fields.Date(string='Last Payment Date', readonly=True, compute="_compute_last_payment_date")

    @api.depends('amount_residual_signed')
    def _compute_last_payment_date(self):
        for record in self:
            if record.payment_state != "not_paid":
                # Buscar la fecha del último pago en account.payment
                if record.type_name == "Vendor Bill":
                    payments = self.env['account.payment'].search([
                        ('ref', '=', record.ref)
                    ], order='date desc')
                    matching_numbers = record.line_ids.mapped('matching_number')

                    # Buscar todas las líneas de apunte que coincidan con los matching_numbers
                    all_payments = self.env['account.move.line'].search([
                        ('matching_number', 'in', matching_numbers),
                        ('account_id.internal_type', 'in', ['receivable', 'payable'])
                    ])
                    # transactions = self.env['payment.transaction'].search([
                    #     ('invoice_ids', 'in', record.ids)
                    # ], order='last_state_change desc')
                else:
                    payments = self.env['account.payment'].search([
                        ('ref', '=', record.name)
                    ], order='date desc')
                
                    # Buscar la fecha del último pago en payment.transaction
                    
                    
                    # Buscar la fecha del último pago en account.move.line
                    all_payments = self.env['account.move.line'].search([
                        ('name', '=', record.name)
                    ], limit=1)

                transactions = self.env['payment.transaction'].search([
                        ('invoice_ids', 'in', record.ids)
                    ], order='last_state_change desc')
                
                if all_payments:
                    move_lines = self.env['account.move.line'].search([
                        ('matching_number', '=', all_payments.matching_number)
                    ], order='date desc')
                else:
                    move_lines = self.env['account.move.line'].browse()

                # Convertir los valores datetime a date
                payment_dates = [
                    fields.Date.to_date(p.date) for p in payments
                ] + [
                    fields.Date.to_date(t.last_state_change) for t in transactions
                ] + [
                    fields.Date.to_date(m.date) for m in move_lines
                ]
                
                if payment_dates:
                    # Asignar la fecha más reciente
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
