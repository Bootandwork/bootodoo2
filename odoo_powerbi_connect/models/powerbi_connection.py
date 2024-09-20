# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

import msal

from odoo import api, fields, models, _
from odoo.exceptions import UserError

required_scopes = ['Workspace.Read.All','Report.Read.All','Dashboard.Read.All','Dataset.Read.All',
                'Workspace.ReadWrite.All','Report.ReadWrite.All','Dashboard.ReadWrite.All',
                'Dataset.ReadWrite.All']

class PowerbiConnection(models.Model):
    _name = "powerbi.connection"
    _inherit = ['mail.thread']
    _description = "Power BI Connection Configuration"
    _rec_name = "instance"

    def _default_api_url(self):
        return "https://api.powerbi.com/v1.0/myorg"
    
    def _default_authorization_url(self):
        return "https://login.microsoftonline.com"

    def _default_instance_name(self):
        return self.env[
            'ir.sequence'].next_by_code('powerbi.connection')
    
    def _default_redirect_uri(self):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url',False)
        self.redirect_uri = f"{base_url}/odoo_connect/instance/{self.id}"

    instance = fields.Char(
        string='Instance Name',
        default=lambda self: self._default_instance_name()
    )
    api_url = fields.Char(
        string='API URL',
        default=lambda self:self._default_api_url(),
        readonly=True,
        required=True
    )
    authority_url = fields.Char(
        string="Authorization URL",
        default=lambda self:self._default_authorization_url(),
        readonly=True,
        required=True
    )
    user = fields.Char(string='Username')
    pwd = fields.Char(string='Password')
    status = fields.Char(string='Status', readonly=True)
    connection_status = fields.Boolean(
        string="Connection Status",
        default=False,
        readonly=True)
    state = fields.Selection(
        [('draft','Draft'),('connected','Connected'),('failed','Failed')],
        string="State",
        default="draft"
    )
    active = fields.Boolean(
        string="Active",
        default=True)
    access_method = fields.Selection(
        [('mu','MasterUser'),('sp','ServicePrincipal')],
        string='Access Method',
        tracking=1,
        required=True,
        default='mu'
    )
    token = fields.Char(string='Token', size=2500)
    client_id = fields.Char(string='Client Id', size=50)
    client_secret = fields.Char(string='Client Secret', size=50)
    tenent_id = fields.Char(string='Tenant Id', size=50, required=True)
    redirect_uri = fields.Char(string='Redirect URI',
        compute=lambda self:self._default_redirect_uri(),
        readonly=True)

    @api.model_create_multi
    def create(self, vals):
        activeConn = self.search([('active','=',True)])
        if (len([True for val in vals if val.get('active')])>1):
            raise UserError(
                _('Warning!\nSorry, Only one active connection is allowed.'))
        for v in range(len(vals)):
            if activeConn and vals[v].get('active'):
                raise UserError(
                    _('Warning!\nSorry, Only one active connection is allowed.'))
            vals[v]['instance'] = self.env[
                'ir.sequence'].next_by_code('powerbi.connection')
        return super().create(vals)
    

    def write(self, vals):
        activeConn = self.search([('active','=',True)])
        if vals.get('active') and (len(self)>1 or len(activeConn-self)>=1):
            raise UserError(
                _('Warning!\nSorry, Only one active connection is allowed.'))
        for instance_obj in self:
            if not instance_obj.instance:
                vals['instance'] = self.env[
                        'ir.sequence'].next_by_code('powerbi.connection')
        return super().write(vals)

    def reset_powerbi_connection(self):
        self.connection_status=False
        self.state='draft'
        self.status='Disconnected'
        
    '''This Method Used To Test Powerbi connection'''
    def test_powerbi_connection(self):
        token = ""
        status=''
        connection_status = False
        text = "Unsuccessful connection, kindly verify your credential!!"
        connection = self._create_powerbi_connection()
        if connection.get("token", ""):
            self.token = str(connection.get("token", ""))
            connection_status = True
            self.state='connected'
            text = connection.get("message", "")
        else:
            status = connection.get("message", "")
            self.state='failed'
        self.status = status
        self.connection_status = connection_status
        if connection.get('consent_url'):
            return {
                "type": "ir.actions.act_url",
                "url": connection.get('consent_url'),
                "target": "new",
            }
        partial = self.env['powerbi.message.wizard'].create({'text': text})
        ctx = dict(self._context or {})
        return {'name': ("Odoo Power BI Connector"),
                'view_mode': 'form',
                'res_model': 'powerbi.message.wizard',
                'view_id': False,
                'res_id': partial.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'context': ctx,
                'target': 'new',
                }

    '''This Method Used To Create a New Powerbi connection at Odoo end'''
    def _create_powerbi_connection(self, scope=[]):
        self.ensure_one()
        text, token, status = "", "", False
        consent_url = ''
        url = f"{self.authority_url}/{self.tenent_id}"
        client_id = self.client_id
        client_secret = self.client_secret
        resource_url = "https://analysis.windows.net/powerbi/api"
        all_scopes = []
        for s in scope:
            all_scopes.append(f"{resource_url}/{s}")
        try:
            app = msal.ConfidentialClientApplication(client_id, client_credential=client_secret, authority=url)
            if self.access_method == "mu":
                user = self.user
                pswd = self.pwd
                if not (user and pswd):
                    return {'token':token, 'message':"Username or Password not set!", 'status':status}
                resp = app.acquire_token_by_username_password(user, pswd, scopes=all_scopes)
            else:
                all_scopes = ["https://analysis.windows.net/powerbi/api/.default"]
                resp = app.acquire_token_for_client(scopes=all_scopes)
            if resp.get("access_token", ""):
                token = "Bearer "+str(resp.get("access_token", ""))
                text = "Test connection successful, now you can proceed with synchronization!!"
                status = True
            else:
                text = "Connection error : "+resp.get("error_description")
                if resp.get("suberror")=="consent_required":
                    allScopes = ''
                    for scp in required_scopes:
                        allScopes+=f'{resource_url}/{scp} '
                    text = """Connection error: The user or administrator has not consented to use the application.
                            Send an interactive authorization request on this url - """
                    consent_url = f"{url}/oauth2/v2.0/authorize?client_id={self.client_id}&response_type=code&redirect_uri={self.redirect_uri}&response_mode=query&scope={allScopes}openid&state=12345"
                    text += consent_url
            return {'token':token, 'message':text, 'status':status, 'consent_url':consent_url}
        except Exception as e:
            return {'status':False, 'message':str(e)}

    def get_active_connection(self):
        domain = [('active','=',True),('connection_status','=',True)]
        connObj = self.search(domain)
        return connObj
    
    '''This Method Used To Update Power BI Credential'''
    def update_credentials(self):
        self.ensure_one()
        partial = self.env['powerbi.credentials.wizard'].create({
            'user': self.user
        })
        return {
            'name': ("Update Power BI Credentials."),
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'powerbi.credentials.wizard',
            'res_id': partial.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'context': self._context,
            'domain': '[]',
        }

    def open_report_wizard(self):
        partial = self.env["powerbi.wizard"].create({})
        ctx = dict(self._context or {})
        ctx['report'] = True
        view_id = self.env.ref('odoo_powerbi_connect.id_powerbi_wizard_view_form').id
        return {'name': "Import Power BI Reports",
                'view_mode': 'form',
                'view_id': view_id,
                'res_model': 'powerbi.wizard',
                'res_id': partial.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'context': ctx,
                'domain': '[]',
                }

    def open_dashboard_wizard(self):
        partial = self.env["powerbi.wizard"].create({})
        ctx = dict(self._context or {})
        ctx['dashboard'] = True
        view_id = self.env.ref('odoo_powerbi_connect.id_powerbi_wizard_view_form').id
        return {'name': "Import Power BI Dashboards",
                'view_mode': 'form',
                'view_id': view_id,
                'res_model': 'powerbi.wizard',
                'res_id': partial.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'context': ctx,
                'domain': '[]',
                }

    '''This Method Used to Import Workspace From Powerbi End'''
    def action_import_workspace(self):
        success = []
        msgModel = self.env["powerbi.message.wizard"]
        scope = ["Workspace.Read.All"]
        connection = self._create_powerbi_connection(scope)
        if connection.get('status'):
            url = f"{self.api_url}/groups"
            resp = self.env["powerbi.synchronization"].callPowerbiApi(url, "get", token=connection.get('token'), scope=scope)
            if resp.get('status'):
                workspaces = resp['value'].get('value',[])
                workspaceModel = self.env["powerbi.workspace"]
                for workspace in workspaces:
                    pid = workspace.get('id','')
                    name = workspace.get('name','')
                    workspaceObj = workspaceModel.search([('powerbi_id', '=', pid)])
                    if not workspaceObj:
                        res = workspaceModel.create({
                                "powerbi_id": pid,
                                "name": name,
                                "is_published": True,
                            })
                        success.append(name)
                if success:
                    message="Workspace name(s) "+str(success)+" successfully imported."
                    self.message_post(body=message)
                if not success:
                    return msgModel.genrated_message("All Workspaces already imported.")
                    
                return msgModel.genrated_message("All Workspaces imported successfully.")
            else:
                message="Workspace import error, Reason: "+resp.get("message")
                self.message_post(body=message)
                return msgModel.genrated_message(resp.get('message'))
        else:
            return msgModel.genrated_message(connection.get('message'))
        

    '''This Method used to Configure Cron at Odoo End'''
    def configure_cron(self):
        self.ensure_one()
        action_cron = self.env.ref("odoo_powerbi_connect.powerbi_export_data_cron")
        return {'name': "Cron",
                'view_mode': 'form',
                'view_id': False,
                'res_model': 'ir.cron',
                'res_id': action_cron.id,
                'type': 'ir.actions.act_window',
                }
