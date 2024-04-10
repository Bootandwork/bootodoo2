from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for order in self:
            order.update_purchase_pricelist()
        return res

    def update_purchase_pricelist(self):
        for order in self:
            for line in order.order_line:
                # pricelist = self.env['product.supplierinfo'].search(
                    # [('partner_id', '=', order.partner_id.id), ('product_tmpl_id', '=', line.product_id.product_tmpl_id.id)])
                # if pricelist:
                    # for price in pricelist:
                        # price.price = line.price_unit
                line.product_id.standard_price = line.price_unit

# class PurchaseOrderLine(models.Model):
#     _inherit = "purchase.order.line"

#     @api.onchange('price_unit')
#     def _onchange_standard_price(self):
#         for rec in self:
#             if rec.price_unit:
#                 rec.product_id.standard_price = rec.price_unit

