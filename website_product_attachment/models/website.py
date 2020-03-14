# -*- coding: utf-8 -*-
from odoo import http, SUPERUSER_ID
from odoo import api, fields, models, _
from odoo.http import request


class website(models.Model):
	_inherit='website'

	def get_product_attachements(self,product_id=None,context=None):
		data=[]
		if product_id:
			attachement_ids=self.env['ir.attachment'].sudo().search([('res_model','=','product.template'),('res_id','=',product_id)])
			if attachement_ids:
				return attachement_ids
		return data

