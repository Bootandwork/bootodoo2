# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

from odoo.exceptions import UserError
from odoo import api, fields, models

class PowerbiWizard(models.TransientModel):
    _name = "powerbi.wizard"
    _description = "Powerbi Wizard"

    workspace_id = fields.Many2one(
        "powerbi.workspace",
        string="Workspace"
    )
    report_id = fields.Many2one(
        "powerbi.report",
        string="Report"
    )
    dashboard_id = fields.Many2one(
        "powerbi.dashboard",
        string="Dashboard"
    )
    
    # fields for data exporting

    exp_workspace_id = fields.Many2one(
        "powerbi.workspace",
        string="Select Workspace"
    )
    exp_table_id = fields.Many2one(
        "powerbi.table",
        string="Table"
    )

    @api.onchange('exp_workspace_id')
    def onchangeExpWorkspace(self):
        active_model = self._context["active_model"]
        return {"domain": {"exp_table_id": [('model_name','=',active_model),('is_published','=',True),('dataset_id.workspace_id.id','=',self.exp_workspace_id.id)]}}

    @api.onchange('workspace_id')
    def onChangeWorkspace(self):
        if self._context.get('dashboard'):
            if self.workspace_id.default_workspace:
                raise UserError('Information: Dashboard embed for default workspace is not supported.')
            return {"domain": {'dashboard_id': [('workspace_id','=',self.workspace_id.id)]}}

    def action_import_report(self):
        success = []
        msgModel = self.env["powerbi.message.wizard"]
        connObj = self.env["powerbi.connection"].get_active_connection()
        if not connObj:
            return msgModel.genrated_message("No active connection found!")
        scope = ["Report.Read.All"]
        connection = connObj._create_powerbi_connection(scope)
        if self.workspace_id.default_workspace:
            url = f"{connObj.api_url}/reports"
        else:
            url = f"{connObj.api_url}/groups/{self.workspace_id.powerbi_id}/reports"
        resp = self.env["powerbi.synchronization"].callPowerbiApi(url, "get", token=connection.get('token'), scope=scope)
       
        if resp.get('status'):
            reports = resp['value'].get('value',[])
            reportModel = self.env["powerbi.report"]
            for report in reports:
                name = report.get('name','')
                pid = report.get('id','')
                reportObj = reportModel.search([('powerbi_id','=',pid)])
                if not reportObj:
                    datsetId=self.env['powerbi.dataset'].search([('powerbi_id','=',report.get('datasetId'))],limit=1)

                    if datsetId.id:
                        res = reportModel.create({
                                "powerbi_id": pid,
                                "name": name,
                                "workspace_id": self.workspace_id.id,
                                "embed_url": report.get("embedUrl",""),
                                'dataset_id': datsetId.id
                                
                            })
                        success.append(name)
            if success:
                message="Report name "+str(success)+" successfully imported."
                connObj.message_post(body=message)
            if not success:
                return msgModel.genrated_message("All reports already imported.")
            return msgModel.genrated_message("All reports successfully imported.")
        else:
            message="Report import error, Reason: "+resp.get("message")
            connObj.message_post(body=message)
            return msgModel.genrated_message(resp.get('message',''))

    def action_import_dashboard(self):
        success = []
        msgModel = self.env["powerbi.message.wizard"]
        connObj = self.env["powerbi.connection"].get_active_connection()
        if not connObj:
            return msgModel.genrated_message("No active connection found!")
        scope = ["Dashboard.ReadWrite.All"]
        connection = connObj._create_powerbi_connection(scope)
        if self.workspace_id.default_workspace:
            url = f"{connObj.api_url}/dashboards"
        else:
            url = f"{connObj.api_url}/groups/{self.workspace_id.powerbi_id}/dashboards"
        resp = self.env["powerbi.synchronization"].callPowerbiApi(url, "get", token=connection.get('token'), scope=scope)
        if resp.get('status'):
            dashboards = resp['value'].get('value',[])
            dashboardModel = self.env["powerbi.dashboard"]
            for dashboard in dashboards:
                name = dashboard.get('displayName','')
                pid = dashboard.get('id','')
                dashboardObj = dashboardModel.search([('powerbi_id','=',pid)])
                if not dashboardObj:
                    res = dashboardModel.create({
                            "powerbi_id": pid,
                            "name": name,
                            "workspace_id": self.workspace_id.id,
                            "embed_url": dashboard.get("embedUrl","")
                        })
                    success.append(name)
            if success:
                message= "Dashboard name(s) "+str(success)+" successfully imported."
                connObj.message_post(body=message)
            if not success:
                return msgModel.genrated_message("All dashboard already imported.")
            return msgModel.genrated_message("All dashboards successfully imported.")
        else:
            message="Dashboard import error, Reason: "+resp.get("message")
            connObj.message_post(body=message)
            return msgModel.genrated_message(resp.get('message',''))

    def start_data_synchronisation(self):
        ctx = dict(self._context or {})
        view_id = self.env.ref("odoo_powerbi_connect.id_powerbi_wizard_export_data_form").id
        return {'name': "Export",
                'view_mode': 'form',
                'view_id': view_id,
                'res_model': 'powerbi.wizard',
                'res_id': False,
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': ctx,
                'domain': '[]',
                }
    
    def action_export(self):
        msgModel = self.env["powerbi.message.wizard"]
        active_ids = self._context["active_ids"]
        workspace = self.exp_workspace_id
        table = self.exp_table_id
        if workspace.id != table.dataset_id.workspace_id.id:
            return msgModel.genrated_message("Error: Table does not belongs to selected workspace.")
        records = self.env[self._context['active_model']].browse(active_ids)
        if table and records:
            return self.export_now(table,records)
    
    def export_now(self, table, records):
        rows = []
        msgModel = self.env["powerbi.message.wizard"]
        connObj = self.env["powerbi.connection"].get_active_connection()
        if not connObj:
            return msgModel.genrated_message("No active connection found!")
        for rec in records:
            rows.append(table.get_row_data(rec))
        if not rows:
            return msgModel.genrated_message("No columns selected in the table.")
        data = {
            "rows" : rows
        }
        scopes = ["Dataset.ReadWrite.All"]
        connection = connObj._create_powerbi_connection(scopes)
        if table.dataset_id.workspace_id.default_workspace:
            url = f"{connObj.api_url}/datasets/{table.dataset_id.powerbi_id}/tables/{table.name}/rows"
        else:
            url = f"{connObj.api_url}/groups/{table.dataset_id.workspace_id.powerbi_id}/datasets/{table.dataset_id.powerbi_id}/tables/{table.name}/rows"
        resp = self.env["powerbi.synchronization"].callPowerbiApi(url, "post", data=data, token=connection.get('token'), scope=scopes)
        if resp.get('status'):
            msg = "Successfully exported."
        else:
            msg = "Error: "+str(resp.get("message"))
        return msgModel.genrated_message(msg)
