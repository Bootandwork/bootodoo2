# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

from odoo import fields, models

class PowerbiReport(models.Model):
    _name = "powerbi.report"
    _description = "Power BI Reports"

    powerbi_id = fields.Char(string='Report Power BI Id', required=True, size=50)
    name = fields.Char(string="Report Name", required=True)
    dataset_id = fields.Many2one(
        "powerbi.dataset",
        string="Dataset",
        required=True
    )
    workspace_id = fields.Many2one("powerbi.workspace",
        string="Workspace",
        required=True)
    embed_url = fields.Char(string="Embed Url", readonly=True, size=500)

    '''This Method Used To Import Report From Powerbi'''
    def get_report(self):
        connObj = self.env["powerbi.connection"].get_active_connection()
        embed_token = {}
        if connObj:
            if not self.embed_url:
                if self.workspace_id.default_workspace:
                    url = f"{connObj.api_url}/reports/{self.powerbi_id}"
                else:
                    url = f"{connObj.api_url}/groups/{self.workspace_id.powerbi_id}/reports/{self.powerbi_id}"
                scope = ["Report.Read.All"]
                connection = connObj._create_powerbi_connection(scope)
                resp = self.env["powerbi.synchronization"].callPowerbiApi(url, "get", token=connection.get("token",""), scope=scope)
                if resp.get('status'):
                    value = resp.get('value')
                    self.embed_url = value.get("embedUrl")
                    self.name = value.get("name")
                else:
                    pass
            scopes = [
                'Report.ReadWrite.All',
                'Dataset.ReadWrite.All'
            ]
            embed_token = self.env["powerbi.synchronization"].get_embed_token("reports", self, connObj, scopes)
        return {"embed_url": self.embed_url, "embed_token": embed_token.get('token',''), "token_expiry": embed_token.get('expiry','')}
