from odoo import models, fields, api
from datetime import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'

    last_payment_date = fields.Date(string='Last Payment Date', readonly=True, compute="_compute_last_payment_date")

    @api.depends('amount_residual_signed')
    def _compute_last_payment_date(self):
        for record in self:
            # Obtener el contenido de invoice_payments_widget que ya es un diccionario
            payments_widget_data = record.invoice_payments_widget

            # Verificar si el campo contiene datos válidos antes de intentar procesarlo
            if payments_widget_data:
                # Obtener la lista de pagos del diccionario
                payments_data = payments_widget_data.get('content', [])

                # Inicializar la variable para la fecha del último pago
                latest_payment_date = None

                # Iterar sobre los pagos para encontrar la fecha más reciente
                for payment in payments_data:
                    payment_date = payment.get('date')

                    if latest_payment_date is None or payment_date > latest_payment_date:
                        latest_payment_date = payment_date

                # Asignar la fecha más reciente encontrada al campo last_payment_date
                record.last_payment_date = latest_payment_date if latest_payment_date else False
            else:
                # Si no hay datos en el campo, establecer last_payment_date como False
                record.last_payment_date = False
