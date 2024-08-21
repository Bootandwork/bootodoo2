from odoo import models, fields, api
from openerp.exceptions import ValidationError
from datetime import datetime
import json

class AccountMove(models.Model):
    _inherit = 'account.move'

    last_payment_date = fields.Date(string='Last Payment Date', readonly=True, compute="_compute_last_payment_date")

    @api.depends('amount_residual_signed')
    def _compute_last_payment_date(self):
        for record in self:
            # Obtener el campo invoice_payments_widget del registro account.move correspondiente
            move = self.env['account.move'].browse(self._context.get('active_id'))
            payments_widget_data = move.invoice_payments_widget

            # Convertir el JSON en una lista de diccionarios
            payments_data = json.loads(payments_widget_data).get('content', [])

            # Inicializar la variable para la fecha del último pago
            latest_payment_date = None

            # Iterar sobre los pagos para encontrar la fecha más reciente
            for payment in payments_data:
                payment_date_str = payment.get('date', '')
                payment_date = datetime.strptime(payment_date_str, '%Y-%m-%d')

                if latest_payment_date is None or payment_date > latest_payment_date:
                    latest_payment_date = payment_date

            # Asignar la fecha más reciente encontrada al campo last_payment_date
            if latest_payment_date:
                record.last_payment_date = latest_payment_date
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
