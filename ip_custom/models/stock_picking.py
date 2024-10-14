from odoo import api, fields, models, _

class StockPicking(models.Model):

    _inherit = "stock.picking"

    ip_validate_control = fields.Boolean(string = "Validate Control", compute="_compute_ip_validate_control")

    @api.depends('picking_type_id.code','state')
    def _compute_ip_validate_control(self):
        for rec in self:
            if rec.sale_id:
                if rec.sale_id.x_studio_shipping_allowd:
                    rec.ip_validate_control = True
                else:
                    if rec.picking_type_id.code == "outgoing":
                        rec.ip_validate_control = True
                    else:
                        rec.ip_validate_control = False
