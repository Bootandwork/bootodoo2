from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    ip_sale_order_count = fields.Integer(string="Pedidos de Venta", compute="_compute_ip_sale_order_count")

    @api.depends('id')
    def _compute_ip_sale_order_count(self):
        for rec in self:
            sale_orders = self.env['sale.order'].search([('partner_id', '=', rec.id), ('state', '=', 'sale')])
            rec.sale_order_count = len(sale_orders)
