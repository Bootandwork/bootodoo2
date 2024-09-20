# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

from odoo import api, fields, models

class PowerbiDataset(models.Model):
    _name = "powerbi.dataset"
    _inherit = ['mail.thread']
    _description = "Power BI Dataset"

    powerbiDatatypes = {
        "char": "string",
        "text": "string",
        "html":'string',
        "selection": "string",
        "float": "Double",
        "integer": "Int64",
        "monetary": "Double",
        "boolean": "bool",
        "many2one": "string",
        "date": "DateTime",
        "datetime": "DateTime",
        "many2many": "string",
        "one2many": "string",
        "json": "string"
    }
    name = fields.Char(string="Dataset Name", required=True, tracking=1)
    powerbi_id = fields.Char(string="Dataset Power BI Id", size=50, readonly=True)
    dataset_type = fields.Selection(
        [('perm','Permanent'),('temp','Temporary')],
        string="Type",
        required=True,
        default="perm",
        tracking=2
    )
    state = fields.Selection(
        [('topublish','To Publish'),('published','Published')],
        compute="_compute_state",
        string="State",
        tracking=3
    )
    is_published = fields.Boolean(string="Is Published", default=False)
    workspace_id = fields.Many2one(
        "powerbi.workspace",
        string="Workspace",
        required=True,
        default=lambda self: self._compute_default_workspace()
    )
    table_ids = fields.One2many(
        "powerbi.table",
        inverse_name="dataset_id",
        string="Tables",
        readonly=True
    )
    count_total_table = fields.Integer(compute='_compute_tables',string='#Tables')

    '''This Method Used to Count Related Tables Of Current Dataset'''
    def _compute_tables(self):
        total_table = self.env['powerbi.table'].search_count([('dataset_id','=',self.id)])
        self.count_total_table = total_table

    def _compute_default_workspace(self):
        return self._context.get('active_id')
   
    @api.depends("is_published")
    def _compute_state(self):
        for rec in self:
            if rec.is_published == True:
                rec.state = "published"
            else:
                rec.state = "topublish"

    '''This Method Used To Redirect To Related Tables of Current Dataset'''
    def action_redirect(self):
        model_name = self._context.get("model_name")
        name = self._context.get("name")
        domain = [('dataset_id','=',self.id)]
        return {
            "type":"ir.actions.act_window",
            'name':name,
            'res_model':model_name,
            'domain':domain,
            'view_mode':'tree,form',
            'target':'current'
            }

    def action_unpublish(self):
        return {
                'name':'Message/Summary',
                'view_mode': 'form',
                'view_id': False,
                'res_model': 'unpublish.message.wizard',
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new'
            }

    '''This Method Used To Unpublish Dataset At Odoo end And Delete At Powerbi End'''
    def unpublish_powerbi(self, dataset_operation, reason):
        msg = ""
        message=''
        msgModel = self.env["powerbi.message.wizard"]
        success, failure = [], []
        scopes = ['Dataset.ReadWrite.All']
        connObj = self.env["powerbi.connection"].get_active_connection()
        connection = connObj._create_powerbi_connection(scopes)
        for dataset in self:
            if dataset_operation == 'delete':
                if dataset.workspace_id.default_workspace:
                    url = f"{connObj.api_url}/datasets/{dataset.powerbi_id}"
                else:
                    url = f"{connObj.api_url}/groups/{dataset.workspace_id.powerbi_id}/datasets/{dataset.powerbi_id}"
                resp = self.env["powerbi.synchronization"].callPowerbiApi(url, 'delete', token=connection.get('token',''), scope=scopes)
                if resp.get('status', False):
                    dataset.powerbi_id = ''
                    dataset.is_published = False
                    dataset.table_ids.is_published = False
                    success.append(dataset.name)
                    message = f'Dataset {dataset.name} successfully deleted from Power BI.<br></br>Reason:- '+reason
                    dataset.message_post(body=message)
                else:
                    failure.append(dataset.name)
                    message = "Dataset could not be deleted.<br></br>Reason:- "+str(resp.get("message"))
                    dataset.message_post(body=message)
            else:
                dataset.powerbi_id=''
                dataset.is_published = False
                dataset.table_ids.is_published = False
                message = f'Dataset {dataset.name} successfully unpublished on odoo.<br></br>Reason:- '+reason
                dataset.message_post(body=message)

        if success:
            msg+=f"{len(success)} dataset(s) successfully unpublished."
        if failure:
            msg+=f"{len(failure)} dataset(s) can't be unpublished."
        
        return msgModel.genrated_message(msg)

    def action_publish(self):
        return self.publish_to_powerbi()

    '''This Method Used To Publish Dataset At Powerbi End'''
    def publish_to_powerbi(self):
        success, failure, already_published, no_tables, invalid = [], [], [], [], []
        msg = ""
        msgModel = self.env["powerbi.message.wizard"]
        connObj = self.env["powerbi.connection"].get_active_connection()
        if not connObj:
            return msgModel.genrated_message("No active connection found!")
        scopes = ['Dataset.ReadWrite.All']
        connection = connObj._create_powerbi_connection(scopes)
        for dataset in self:
            if dataset.table_ids.filtered(lambda t: t.use_relation and not t.validate_table_relation()):
                invalid.append(dataset.id)
                continue
            if dataset.is_published:
                already_published.append(dataset.id)
                continue
            if dataset.workspace_id.default_workspace:
                url = f"{connObj.api_url}/datasets"
            else:
                url = f"{connObj.api_url}/groups/{dataset.workspace_id.powerbi_id}/datasets"
            tables = dataset.get_tables_data()
            if not tables:
                no_tables.append(dataset.id)
                continue
            data = {
                "name": dataset.name,
                "defaultMode": "Push" if dataset.dataset_type == "perm" else "Streaming",
                "tables": tables,
                "relationships": dataset.get_tables_relation()
            }
            resp = self.env["powerbi.synchronization"].callPowerbiApi(url, 'post', data, connection.get('token',''), scopes)
            if resp.get('status', False):
                value = resp.get('value')
                dataset.powerbi_id = value.get('id','')
                dataset.is_published = True
                dataset.table_ids.is_published = True
                success.append(dataset.name)
                message = f'Dataset {dataset.name} successfully published to Power BI.'
                dataset.message_post(body=message)
            else:
                failure.append(dataset.name)
                message = "Dataset could not be published.<br></br>Reason:- "+str(resp.get("message"))
                dataset.message_post(body=message)

        if success:
            msg+=f"{len(success)} dataset(s) successfully published."
        if failure:
            msg+=f"{len(failure)} dataset(s) failed to publish."
        if already_published:
            msg+=f"{len(already_published)} dataset(s) already published."
        if no_tables:
            msg+=f"{len(no_tables)} dataset(s) doesn't contain any table."
        if invalid:
            msg+=f"{len(invalid)} dataset(s) tables are not valid."
        return msgModel.genrated_message(msg)

    def get_tables_data(self):
        return_data = []
        for table in self.table_ids:
            table_data = {
                "name" : table.name,
                "columns" : self.get_table_columns(table)
            }
            return_data.append(table_data)
        return return_data

    '''This Method Used To Get Table Column Data'''
    def get_table_columns(self,table):
        columns = [{"name": "Id", "dataType": "string"}]
        for col in table.column_ids:
            columns.append({
                "name" : col.label,
                "dataType" : self.powerbiDatatypes.get(col.field_type, 'string')
            })
        return columns

    def get_tables_relation(self):
        self.ensure_one
        relations = []
        for table in self.table_ids.filtered(lambda t: t.use_relation):
            for column in table.column_ids.filtered(lambda c: c.field_type == 'many2one'):
                related_table = self.table_ids.filtered(lambda t: t.model_id.model == column.field_id.relation)
                if related_table-table:
                    relations.append({
                        'fromColumn': column.label,
                        'fromTable': table.name,
                        'name': f"{table.name} to {related_table.name} relation",
                        'toColumn': 'Id',
                        'toTable': related_table.name
                    })
        return relations
