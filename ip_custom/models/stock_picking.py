from odoo import api, fields, models, _

class StockPicking(models.Model):

    _inherit = "stock.picking"

    ip_validate_control = fields.Boolean(string = "Validate Control", compute="_compute_ip_validate_control", store=True)

    @api.depends('picking_type_id.code', 'sale_id', 'sale_id.x_studio_shipping_allowd')
    def _compute_ip_validate_control(self):
        for rec in self:
            # Default the control to False
            rec.ip_validate_control = False

            # Check if there is a related sale order
            if rec.sale_id:
                # If x_studio_shipping_allowd is True, set control to True
                if rec.sale_id.x_studio_shipping_allowd:
                    rec.ip_validate_control = True
                else:
                    rec.ip_validate_control = False
                # Otherwise, check if picking type is 'outgoing'
            else:
                # If no sale order, check if picking type is 'outgoing'
                if rec.picking_type_id.code == "outgoing":
                    rec.ip_validate_control = True

                else:
                    rec.ip_validate_control = False
