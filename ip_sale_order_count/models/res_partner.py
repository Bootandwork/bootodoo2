from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    ip_sale_order_count = fields.Integer(string="Sale Order Count", compute="_compute_ip_sale_order_count")

    @api.depends('sale_order_ids.state')
    def _compute_ip_sale_order_count(self):
        for rec in self:
            sale_orders = self.env['sale.order'].search([('partner_id', '=', rec.id), ('state', '=', 'sale')])
            rec.ip_sale_order_count = len(sale_orders)
