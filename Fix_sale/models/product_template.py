# -*- coding: utf-8 -*-
#############################################################################

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_attribute_exclusions(self, parent_combination=None, parent_name=None):
        res = super()._get_attribute_exclusions(parent_combination=parent_combination,
                                                parent_name=parent_name)
        return {
            'exclusions': res.get('exclusions'),
            'archived_combinations': res.get('archived_combinations'),
            'parent_exclusions': res.get('parent_exclusions'),
            'parent_product_name': res.get('parent_product_name'),
            'mapped_attribute_names': res.get('mapped_attribute_names')
        }
