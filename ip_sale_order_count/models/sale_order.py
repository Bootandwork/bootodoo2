from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    ip_sale_order_count = fields.Integer(string="Sale Order Count", related="partner_id.ip_sale_order_count")
