# -*- coding: utf-8 -*-

from odoo import fields, models, api

class MrpBom(models.Model):
    _inherit="mrp.bom"

    def update_bom_product_cost(self):
        for rec in self:
            temp_list=[]
            if rec.bom_line_ids:
                for first_bom in rec.bom_line_ids:
                    temp_list.append(first_bom.product_tmpl_id)
                for record in temp_list:
                    bom=self.env['mrp.bom'].search([('product_tmpl_id','=',record.id)],limit=1)
                    if bom.bom_line_ids:
                        for record in bom.bom_line_ids:
                            temp_list.append(record.product_tmpl_id)
            if temp_list:
                for cost_update in reversed(temp_list):
                    cost_update.button_bom_cost()
            rec.product_tmpl_id.button_bom_cost()
            if rec.product_id:
                rec.product_id.button_bom_cost()

class Product(models.Model):
    _inherit="product.product"

    def update_bom_product_cost(self):
        for product in self:
            if product.bom_ids:
                for rec in product.bom_ids:
                    temp_list=[]
                    if rec.bom_line_ids:
                        for first_bom in rec.bom_line_ids:
                            temp_list.append(first_bom.product_tmpl_id)
                        for record in temp_list:
                            bom=self.env['mrp.bom'].search([('product_tmpl_id','=',record.id)],limit=1)
                            if bom.bom_line_ids:
                                for record in bom.bom_line_ids:
                                    temp_list.append(record.product_tmpl_id)
                    if temp_list:
                        for cost_update in reversed(temp_list):
                            cost_update.button_bom_cost()
                    rec.product_tmpl_id.button_bom_cost()
                    if rec.product_id:
                        rec.product_id.button_bom_cost()

    """
    @api.model
    def create(self,vals):
        res = super(MrpBom,self).create(vals)
        res.update_bom_product_cost()
        domain = [('product_id', '=', res.product_id.id),('order_id.state', '=', 'draft')]
        find_sol = self.env['sale.order.line'].search(domain)
        for data in find_sol:
            data._compute_purchase_price()
        return res

    def write(self,vals):
        res = super(MrpBom,self).write(vals)
        for rec in self:
            rec.update_bom_product_cost()
            domain = [('product_id', '=', rec.product_id.id),('order_id.state', '=', 'draft')]
            find_sol = self.env['sale.order.line'].search(domain)
            for data in find_sol:
                data._compute_purchase_price()
        return res
    """
    