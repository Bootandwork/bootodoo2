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
from odoo.exceptions import ValidationError

class PowerbiWorkspace(models.Model):
    _name = "powerbi.workspace"
    _inherit = ['mail.thread']
    _description = "Power BI Workspace/Group"

    name = fields.Char(string="Workspace Name", required=True, tracking=1)
    powerbi_id = fields.Char(string="Workspace Power BI Id", size=50, readonly=True)
    state = fields.Selection(
        [('topublish','To Publish'),('published','Published')],
        compute="_compute_state",
        string="State",
        tracking=2
    )
    is_published = fields.Boolean(string="Is Published", default=False)
    default_workspace = fields.Boolean(string="Default Workspace", default=False)
    responsible_user = fields.Many2one('res.users', string="Responsible", tracking=3)
    count_total_dataset = fields.Integer(compute='_compute_totals', string='Datasets')
    count_total_report = fields.Integer(compute='_compute_totals',string='Reports')
    count_total_dashboard = fields.Integer(compute='_compute_totals',string='Dashboards')

    '''This Method Used to Count Related Datasets, Reports and Dashboards Of Current Workspace'''
    def _compute_totals(self):
        total_dataset = self.env['powerbi.dataset'].search_count([('workspace_id','=',self.id)])
        total_report = self.env['powerbi.report'].search_count([('workspace_id','=',self.id)])
        total_dashboard = self.env['powerbi.dashboard'].search_count([('workspace_id','=',self.id)])
        self.count_total_dataset = total_dataset
        self.count_total_report = total_report
        self.count_total_dashboard = total_dashboard

    '''This Method Used To Redirect To Related Dataset And Table of Current Workspace'''
    def action_redirect(self):
        model_name = self._context.get("model_name")
        name = self._context.get("name")
        domain = [('workspace_id','=',self.id)]
        return {
            "type":"ir.actions.act_window",
            'name':name,
            'res_model':model_name,
            'domain':domain,
            'view_mode':'tree,form',
            'target':'current'
            }

   
    @api.model_create_multi
    def create(self, vals):
        if (len([True for val in vals if val.get('default_workspace')])>1):
            raise ValidationError('Warning: Can\'t create more than 1 default workspace.')
        recs = self.search([('default_workspace','=',True)])
        for val in vals:
            if val.get('default_workspace'):
                if len(recs) > 0:
                    raise ValidationError('Warning: Can\'t create more than 1 default workspace.')
        return super(PowerbiWorkspace, self).create(vals)
    
    def write(self, vals):
        if vals.get('default_workspace'):
            if len(self)>1:
                raise ValidationError('Warning: Can\'t create more than 1 default workspace.')
            else:
                recs = self.search([('default_workspace','=',True)])
                recs -= self
                if len(recs) > 0:
                    raise ValidationError('Warning: Can\'t create more than 1 default workspace.')
        return super(PowerbiWorkspace, self).write(vals)

    @api.depends("is_published")
    def _compute_state(self):
        for rec in self:
            if rec.is_published == True:
                rec.state = "published"
            else:
                rec.state = "topublish"

    def action_publish(self):
        return self.publish_to_powerbi()
    
    '''This Method Used to Publish Workspaces at Power BI End '''
    def publish_to_powerbi(self):
        success, failure, already_published = [], [], []
        msg = ""
        msgModel = self.env["powerbi.message.wizard"]
        connObj = self.env["powerbi.connection"].get_active_connection()
        if not connObj:
            return msgModel.genrated_message("No active connection found!")

        url = f"{connObj.api_url}/groups"
        scopes = ['Workspace.ReadWrite.All']
        connection = connObj._create_powerbi_connection(scopes)
        for workspace in self:
            if workspace.default_workspace:
                continue
            if workspace.is_published:
                already_published.append(workspace.id)
                continue
            data = {
                "name": workspace.name,
            }
            resp = self.env["powerbi.synchronization"].callPowerbiApi(url, 'post', data, connection.get('token',''), scopes)
            if resp.get('status', False):
                value = resp.get('value')
                workspace.powerbi_id = value.get('id','')
                workspace.is_published = True
                success.append(workspace.name)
            else:
                failure.append(workspace.id)
                res = ast.literal_eval(resp.get("message"))
                msg+="Workspace export error"+": Reason - "+str((res.get("error")).get("code"))
                
        if success:
            msg+=f"workspace {str(success)}  successfully published."
        if already_published:
            msg+=f"{len(already_published)} workspaces(s) are already published."
        
        return msgModel.genrated_message(msg)

    '''This Method Use To Create Demo Data'''
    @api.model
    def _create_sale_order_data(self):
        saleModule = self.env["ir.module.module"].search([('name','=','sale'),('state','=','installed')],limit=1)
        if saleModule:
            modelObj = self.env["ir.model"].search([("model","=","sale.order")],limit=1)
            model = modelObj.model
            workspace = self.search([('default_workspace','=',True)],limit=1)
            if not workspace:
                workspace = self.create({"name": "My Workspace", "default_workspace": True, "is_published": True})
            dataset = self.env["powerbi.dataset"].create({
                "name": "Odoo Sales",
                "dataset_type": "perm",
                "workspace_id": workspace.id
            })
            table = self.env["powerbi.table"].create({
                "name": "Sales",
                "dataset_id": dataset.id,
                "model_id": modelObj.id,
                "model_name": model
            })
            self._create_table_column(model, table,[
                "name"
                "amount_total"
                "date_order"
            ])
        return True

    @api.model
    def _create_invoice_data(self):
        invModule = self.env["ir.module.module"].search([('name','=','account'),('state','=','installed')],limit=1)
        if invModule:
            modelObj = self.env["ir.model"].search([("model","=","account.move")],limit=1)
            model = modelObj.model
            workspace = self.search([('default_workspace','=',True)],limit=1)
            if not workspace:
                workspace = self.create({"name": "My Workspace", "default_workspace": True, "is_published": True})
            dataset = self.env["powerbi.dataset"].create({
                "name": "Odoo Invoices",
                "dataset_type": "perm",
                "workspace_id": workspace.id
            })
            table = self.env["powerbi.table"].create({
                "name": "Invoices",
                "dataset_id": dataset.id,
                "model_id": modelObj.id,
                "model_name": model
            })
            self._create_table_column(model, table,[
                "name"
                "amount_total"
                "invoice_date"
                "invoice_origin"
                "move_type"
            ])
        return True

    @api.model
    def _create_stock_data(self):
        stockModule = self.env["ir.module.module"].search([('name','=','stock'),('state','=','installed')],limit=1)
        if stockModule:
            modelObj = self.env["ir.model"].search([("model","=","stock.move")],limit=1)
            model = modelObj.model
            workspace = self.search([('default_workspace','=',True)],limit=1)
            if not workspace:
                workspace = self.create({"name": "My Workspace", "default_workspace": True, "is_published": True})
            dataset = self.env["powerbi.dataset"].create({
                "name": "Odoo Inventory",
                "dataset_type": "perm",
                "workspace_id": workspace.id
            })
            table = self.env["powerbi.table"].create({
                "name": "Inventory",
                "dataset_id": dataset.id,
                "model_id": modelObj.id,
                "model_name": model
            })
            self._create_table_column(model, table,[
                "name"
                "origin"
                "price_unit"
            ])
        return True

    @api.model
    def _create_purchase_data(self):
        purchaseModule = self.env["ir.module.module"].search([('name','=','purchase'),('state','=','installed')],limit=1)
        if purchaseModule:
            modelObj = self.env["ir.model"].search([("model","=","purchase.order")],limit=1)
            model = modelObj.model
            workspace = self.search([('default_workspace','=',True)],limit=1)
            if not workspace:
                workspace = self.create({"name": "My Workspace", "default_workspace": True, "is_published": True})
            dataset = self.env["powerbi.dataset"].create({
                "name": "Odoo Purchase",
                "dataset_type": "perm",
                "workspace_id": workspace.id
            })
            table = self.env["powerbi.table"].create({
                "name": "Purchase",
                "dataset_id": dataset.id,
                "model_id": modelObj.id,
                "model_name": model
            })
            self._create_table_column(model, table,[
                "name"
                "origin"
                "amount_total"
                "date_order"
            ])
        return True

    @api.model
    def _create_pos_data(self):
        posModule = self.env["ir.module.module"].search([('name','=','point_of_sale'),('state','=','installed')],limit=1)
        if posModule:
            modelObj = self.env["ir.model"].search([("model","=","pos.order")],limit=1)
            model = modelObj.model
            workspace = self.search([('default_workspace','=',True)],limit=1)
            if not workspace:
                workspace = self.create({"name": "My Workspace", "default_workspace": True, "is_published": True})
            dataset = self.env["powerbi.dataset"].create({
                "name": "Odoo POS",
                "dataset_type": "perm",
                "workspace_id": workspace.id
            })
            table = self.env["powerbi.table"].create({
                "name": "POS",
                "dataset_id": dataset.id,
                "model_id": modelObj.id,
                "model_name": model
            })
            self._create_table_column(model, table, [
                "name"
                "amount_total"
                "date_order"
            ])
        return True
            
    '''This Method Used to Create Table Column For Demo Data'''
    def _create_table_column(self, model, table, fields):
        for field in fields:
            field_id = self.env["ir.model.fields"].search([('model_id.model','=',model),('name','=',field)],limit=1)
            self.env["powerbi.table.column"].create({
                "table_id": table.id,
                "field_id": field_id.id,
                "field_type": field_id.ttype
            })
