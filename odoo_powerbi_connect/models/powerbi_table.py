# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

import ast
from odoo import api, fields, models

count=10000

class PowerbiTable(models.Model):
    _name = "powerbi.table"
    _inherit = ['mail.thread']
    _description = "Powerbi Table"

    name = fields.Char(string="Table Name", required=True, tracking=1)
    dataset_id = fields.Many2one(
        "powerbi.dataset",
        string="Dataset",
        domain="[('is_published','!=',True)]",
        required=True, default=lambda self: self._compute_default_dataset())
    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        ondelete="set null",
        tracking=2
    )
    model_name = fields.Char(string="Model Name")
    column_ids = fields.One2many(
        "powerbi.table.column",
        inverse_name="table_id",
        string="Table Fields",
    )
    filter_domain = fields.Char(string="Domain")
    state = fields.Selection(
        [('topublish','To Publish'),('published','Published')],
        compute="_compute_state",
        string="State",
        tracking=3
    )
    is_published = fields.Boolean(string="Is Published", default=False)
    is_modified = fields.Boolean(string="Modified", default=False)
    run_cron = fields.Boolean(string="Export Data Using Cron",
                help='On Activation of this option table data automatic export powerbi end ', default=False)
    export_action = fields.Integer(string="Action Id", default=0)
    last_sync_datetime = fields.Datetime("Last Sync Datetime", 
        help="This Datetime will be used during export operation./nThe records created after this date will be exported to powerbi./nThis will be updated after every export operation.")
    use_relation = fields.Boolean("Use Table Relationship", default=False,
        help="Check this field if you want to manage relationship for this table based on primary key and foreign key (by Many2one field).")

    _sql_constraints = [
        (
            'dataset_table_unique',
            'unique (dataset_id,name)',
            'Table name must be unique per dataset.',
        )
    ]

    def _compute_default_dataset(self):
        if not self.env['powerbi.dataset'].browse(self._context.get('active_id')).is_published:
            return self._context.get('active_id')
        else:
            return 0

    def _compute_default_dataset(self):
        if not self.env['powerbi.dataset'].browse(self._context.get('active_id')).is_published:
            return self._context.get('active_id')
        else:
            return 0

    @api.depends("is_published")
    def _compute_state(self):
        for rec in self:
            if rec.is_published == True:
                rec.state = "published"
            else:
                rec.state = "topublish"

    @api.onchange("model_id")
    def onchange_model(self):
        self.model_name = self.model_id.model
        self.column_ids = [(6,0,[])]
        model = self.model_id.model
        if model == "sale.order":
            self._create_column(model, [
                "name",
                "amount_total",
                "date_order",
            ])
        elif model == "account.move":
            self._create_column(model, [
                "name",
                "invoice_origin",
                "amount_total",
                "invoice_date",
                "move_type"
            ])
        elif model == "stock.move":
            self._create_column(model, [
                "name",
                "origin",
                "price_unit",
            ])

    def _create_column(self, model, fields):
        for field in fields:
            field_id = self.env["ir.model.fields"].search([('model_id.model','=',model),('name','=',field)],limit=1)
            self.env["powerbi.table.column"].create({
                "table_id": self.id,
                "field_id": field_id.id,
                "field_type": field_id.ttype,
                "label": field_id.field_description
            })

    def write(self, vals):
        if "column_ids" in vals:
            vals.update(is_modified=True)
        return super(PowerbiTable, self).write(vals)

    def action_export(self):
        return {
                'name':'Message/Summary',
                'view_mode': 'form',
                'view_id': False,
                'res_model': 'powerbi.table.wizard',
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
                "context":{'default_operation':'export'}
            }
      
    
    def action_delete(self):
        return {
                'name':'Message/Summary',
                'view_mode': 'form',
                'view_id': False,
                'res_model': 'powerbi.table.wizard',
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
                "context":{'default_operation':'delete'}
            }
    
    def action_update_schema(self):
        return {
                'name':'Message/Summary',
                'view_mode': 'form',
                'view_id': False,
                'res_model': 'powerbi.table.wizard',
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
                "context":{'default_operation':'update'}
            }

    def export_to_powerbi(self):
        success, failure, not_published, no_data = [], [], 0, 0
        msg = ""
        msgModel = self.env["powerbi.message.wizard"]
        connObj = self.env["powerbi.connection"].get_active_connection()
        if not connObj:
            return msgModel.genrated_message("No active connection found!")
        scopes = ["Dataset.ReadWrite.All"]
        connection = connObj._create_powerbi_connection(scopes)
        for table in self:
            if not table.is_published:
                not_published += 1
                continue
            model = self.env[table.model_id.model]
            domain = []
            if table.filter_domain:
                domain = ast.literal_eval(table.filter_domain)
            
            if domain and table.last_sync_datetime:
                domain = ['&'] + [('create_date','>',table.last_sync_datetime)] + domain
            elif table.last_sync_datetime:
                domain = [('create_date','>',table.last_sync_datetime)]
            table.last_sync_datetime = fields.Datetime.now()
            records = model.search(domain)
            rows = []
            for rec in records:
                rows.append(table.get_row_data(rec))
            if not rows:
                no_data += 1
                continue
            if table.dataset_id.workspace_id.default_workspace:
                url = f"{connObj.api_url}/datasets/{table.dataset_id.powerbi_id}/tables/{table.name}/rows"
            else:
                url = f"{connObj.api_url}/groups/{table.dataset_id.workspace_id.powerbi_id}/datasets/{table.dataset_id.powerbi_id}/tables/{table.name}/rows"
            global count
            tempRows = rows[:count] if len(rows) > count else rows
            while tempRows:
                data = {
                    "rows" : tempRows
                }
                resp = self.env["powerbi.synchronization"].callPowerbiApi(url, "post", data=data, token=connection.get('token'), scope=scopes)
                if resp.get('status'):
                    message="Table Data successfully exported to Power Bi."
                    table.message_post(body=message)
                    if table.id not in success:
                        success.append(table.id)
                else:
                    if table.id not in failure:
                        failure.append(table.id)
                    message= "Table data could not be exported.<br></br>Reason:- "+str(resp.get("message"))
                    table.message_post(body=message)
                    
                if len(rows) > len(tempRows):
                    tempRows = rows[count:count+10000] if len(rows) > count+10000 else rows[count:]
                    count += 10000
                else:
                    tempRows = []
        if success:
            msg+=f"{len(success)} table data successfully exported."
        if failure:
            msg+=f"{len(failure)} table data can't be exported."
        if not_published:
            msg+=f"{not_published} tables not published yet."
        if no_data:
            msg+=f"{no_data} tables have no data to export."
        
        return msgModel.genrated_message(msg)

    def get_row_data(self, dataObj):
        self.ensure_one()
        row = {'Id': dataObj.id}
        for column in self.column_ids:
            value = getattr(dataObj, column.name)
            if column.field_type == 'many2one':
                row[column.label] = value and value.id
            else:
                row[column.label] = value or '' if column.field_type in ['date','datetime'] else value
        return row

    def delete_powerbi_data(self):
        success, failure, not_published = [], [], 0
        msg = ""
        msgModel = self.env["powerbi.message.wizard"]
        connObj = self.env["powerbi.connection"].get_active_connection()
        if not connObj:
            return msgModel.genrated_message("No active connection found!")
        scopes = ["Dataset.ReadWrite.All"]
        connection = connObj._create_powerbi_connection(scopes)
        for table in self:
            if not table.is_published:
                not_published += 1
                continue
            if table.dataset_id.workspace_id.default_workspace:
                url = f"{connObj.api_url}/datasets/{table.dataset_id.powerbi_id}/tables/{table.name}/rows"
            else:
                url = f"{connObj.api_url}/groups/{table.dataset_id.workspace_id.powerbi_id}/datasets/{table.dataset_id.powerbi_id}/tables/{table.name}/rows"
            resp = self.env["powerbi.synchronization"].callPowerbiApi(url, "delete", token=connection.get('token',''), scope=scopes)
            if resp.get('status'):
                success.append(table.id)
                table.last_sync_datetime = False
                message="Table data successfully deleted on Power BI"
                table.message_post(body=message)
            else:
                failure.append(table.id)
                message="Table data could not be deleted.<br></br>Reason:- "+str(resp.get("message"))
                table.message_post(body=message)
               
        if success:
            msg+=f"{len(success)} table data successfully deleted."
            
        if failure:
            msg+=f"{len(failure)} table data can't be deleted."
        if not_published:
            msg+=f"{not_published} tables not published yet."
        
        return msgModel.genrated_message(msg)

    def update_table_schema(self):
        success, failure, not_published, no_columns, invalid = [], [], 0, 0, 0
        msg = ""
        msgModel = self.env["powerbi.message.wizard"]
        connObj = self.env["powerbi.connection"].get_active_connection()
        if not connObj:
            return msgModel.genrated_message("No active connection found!")
        scopes = ["Dataset.ReadWrite.All"]
        connection = connObj._create_powerbi_connection(scopes)
        for table in self:
            if not table.is_published:
                not_published += 1
                continue
            if table.use_relation and not table.validate_table_relation():
                invalid += 1
                continue
            columns = self.env["powerbi.dataset"].get_table_columns(table)
            if not columns:
                no_columns += 1
                continue
            data = {
                "name": table.name,
                "columns": columns
            }
            if table.dataset_id.workspace_id.default_workspace:
                url = f"{connObj.api_url}/datasets/{table.dataset_id.powerbi_id}/tables/{table.name}"
            else:
                url = f"{connObj.api_url}/groups/{table.dataset_id.workspace_id.powerbi_id}/datasets/{table.dataset_id.powerbi_id}/tables/{table.name}"
            resp = self.env["powerbi.synchronization"].callPowerbiApi(url, "put", data=data, token=connection.get('token'), scope=scopes)
            if resp.get('status'):
                table.is_modified = False
                success.append(table.id)
                message="Table schema successfully updated on Power BI"
                table.message_post(body=message)
            else:
                failure.append(table.id)
                message="Table schema could not be updated<br></br>Reason:- "+str(resp.get("message"))
                table.message_post(body=message)
        if success:
            msg+=f"{len(success)} tables successfully updated.\n"
            
        if failure:
            msg+=f"{len(failure)} tables can't be updated.\n"
        if not_published:
            msg+=f"{not_published} tables not published yet.\n"
        if no_columns:
            msg+=f"{no_columns} tables does not have any columns to update.\n"
        if invalid:
            msg+=f"{invalid} tables are not valid.\n"
        
        return msgModel.genrated_message(msg)

    def open_column_wizard(self):
        partial = self.env["table.column.wizard"].create({})
        ctx = dict(self._context or {})
        ctx['active_id']=self.id
        ctx['domain_model_name'] = self.model_id.model
        ctx['map_ids'] = [col.field_id.id for col in self.column_ids]
        return {'name': "Add Column",
                'view_mode': 'form',
                'view_id': False,
                'res_model': 'table.column.wizard',
                'res_id': partial.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'context': ctx,
                'domain': '[]',
                }
   
    '''This Method Used to Add Server Action For Specific Table'''
    def create_server_action(self):
        self.ensure_one()
        model_id = self.model_id.id
        name = self.model_id.name
        existing_action = self.search([('model_id','=',model_id),
                                    ('export_action','!=',0)],limit=1)
        if not existing_action:
            message = 'Message: Server Action Created Succesfully For Model %s'%name
            code = "action = env['powerbi.wizard'].start_data_synchronisation()"
            action_server = False
            try:
                action_server = self.env['ir.actions.server'].create({
                    'name':'Export To Powerbi',
                    'model_id': model_id,
                    'state':'code',
                    'binding_model_id': model_id,
                    'code': code
                })
            except Exception as e:
                message= 'Message: Error While Creating Server Action: %s'%str(e)
            if action_server:
                self.export_action = action_server.id
        else:
            message = 'Message: Server Action Is Already Created For The Model %s'%name
        return self.env['powerbi.message.wizard'].genrated_message(message)

    '''This Method Used to Delete Server Action For Specific Table'''
    def delete_server_action(self):
        self.ensure_one()
        model_id = self.model_id.id
        name = self.model_id.name
        existing_action = self.search([('model_id','=',model_id),
                                    ('export_action','!=',0)],limit=1)

        if existing_action:
            message = 'Server Action deleted successfully for model %s'%name
            action_server = self.env['ir.actions.server'].search([('id','=',existing_action.export_action)])
            if action_server:
                try:
                    res = action_server.unlink()
                    if res:
                        existing_action.export_action = 0
                except Exception as e:
                    message = 'Error while deleting server action: %s'%str(e)
            else:
                message = "No server action found for the model %s"%name
        else:
            message = "No server action found for the model %s"%name
        return self.env["powerbi.message.wizard"].genrated_message(message)

    '''This method is used to export data via cron.'''
    @api.model
    def powerbi_export_cron(self):
        tables = self.search([("is_published","=",True),("run_cron","=",True),("is_modified","=",False)])
        if tables:
            tables.export_to_powerbi()
        return True

    def validate_table_relation(self):
        self.ensure_one()
        for column in self.column_ids.filtered(lambda c: c.field_type == 'many2one'):
            related_table = self.dataset_id.table_ids.filtered(lambda d: d.model_id.model == column.field_id.relation)
            if not related_table:
                self.message_post(body=f"No table found for model {column.field_id.relation} in dataset {self.dataset_id.name}")
                return False, 
        return True
