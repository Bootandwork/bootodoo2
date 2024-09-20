# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class TableColumnWizard(models.TransientModel):
    _name = "table.column.wizard"
    _description = "Column Wizard"

    field_id = fields.Many2one(
        "ir.model.fields",
        string="Field"
    )
    field_type = fields.Selection(string="Type", related="field_id.ttype")
    label = fields.Char(string="Label")

    @api.onchange('field_id')
    def onchange_field(self):
        self.label = self.field_id.field_description

    def action_add_column(self):
        if not self.field_id:
            raise ValidationError("Kindly select a field!")
        res = self.env["powerbi.table.column"].create({
            "table_id": self._context['active_id'],
            "field_id": self.field_id.id,
            "field_type": self.field_type,
            "label": self.label or self.field_id.field_description
        })
        return True
