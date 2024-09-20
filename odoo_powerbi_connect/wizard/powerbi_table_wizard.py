# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

from odoo import fields, models

class PowerbiTableWizard(models.TransientModel):
    _name = "powerbi.table.wizard"
    _description = "PowerBi Table Wizard"
    
    operation = fields.Text(string='Operation', readonly=True, translate=True)

    def update_table(self):
        if self.operation=='export':
            return self.env['powerbi.table'].browse(self._context.get('active_ids')).export_to_powerbi()
        elif self.operation=='delete':
            return self.env['powerbi.table'].browse(self._context.get('active_ids')).delete_powerbi_data()
        elif self.operation=='update':
            return self.env['powerbi.table'].browse(self._context.get('active_ids')).update_table_schema()
        else:
            return self.env['powerbi.message.wizard'].genrated_message('Wrong operation selected kindly verify again.')
