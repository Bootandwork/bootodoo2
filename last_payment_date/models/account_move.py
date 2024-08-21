from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    last_payment_date = fields.Date(string='Last Payment Date', readonly=True, compute="_compute_last_payment_date")

    @api.depends('amount_residual_signed')
    def _compute_last_payment_date(self):
        for record in self:
            if record.payment_state != "not_paid":
                # Buscar la fecha del último pago en account.payment
                if record.move_type == "in_invoice":
                    payments = self.env['account.payment'].search([
                        ('ref', '=', record.ref)
                    ], order='date desc')
                    all_payments = self.env['account.move.line'].search([
                        ('name', 'ilike', record.ref)
                    ])
                else:
                    payments = self.env['account.payment'].search([
                        ('ref', '=', record.name)
                    ], order='date desc')

                    # Buscar la fecha del último pago en account.move.line
                    all_payments = self.env['account.move.line'].search([
                        ('name', 'ilike', record.name)
                    ])

                transactions = self.env['payment.transaction'].search([
                    ('invoice_ids', 'in', record.ids)
                ], order='last_state_change desc')

                if all_payments:
                    move_lines = self.env['account.move.line'].search([
                        ('matching_number', '=', all_payments[0].matching_number)
                    ], order='date desc')
                else:
                    move_lines = self.env['account.move.line'].browse()

                # Verificar y convertir las fechas
                payment_dates = []
                for p in payments:
                    if p.date:
                        payment_dates.append(fields.Date.to_date(p.date))
                    else:
                        raise UserError(f"Fecha inválida en payment: {p}")

                for t in transactions:
                    if t.last_state_change:
                        payment_dates.append(fields.Date.to_date(t.last_state_change))
                    else:
                        raise UserError(f"Fecha inválida en transaction: {t}")

                for m in move_lines:
                    if m.date:
                        payment_dates.append(fields.Date.to_date(m.date))
                    else:
                        raise UserError(f"Fecha inválida en move_line: {m}")

                if payment_dates:
                    # Asignar la fecha más reciente
                    record.last_payment_date = max(payment_dates)
                else:
                    record.last_payment_date = False
            else:
                record.last_payment_date = False
