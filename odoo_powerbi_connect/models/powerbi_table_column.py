# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

from odoo import fields, models

class PowerbiTableColumn(models.Model):
    _name = "powerbi.table.column"
    _description = "Power BI Table Columns"

    name = fields.Char(string="Name", related="field_id.name")
    table_id = fields.Many2one(
        "powerbi.table",
        string="Table"
    )
    field_id = fields.Many2one(
        "ir.model.fields",
        string="Field"
    )
    field_type = fields.Char(string="Type")
    label = fields.Char(string="Label")

    def create(self, vals):
        res = super(PowerbiTableColumn, self).create(vals)
        if res and vals.get("table_id"):
            table = self.env["powerbi.table"].browse(vals.get("table_id"))
            table.is_modified = True
        return res
