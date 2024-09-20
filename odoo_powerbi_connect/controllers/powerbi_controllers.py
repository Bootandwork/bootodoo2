# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

from odoo import http
from odoo.http import request

class PowerbiControllers(http.Controller):

    @http.route("/get/reportparameter", auth="user", type="json")
    def get_report_parameter(self, res_id, **kw):
        reportObj = request.env['powerbi.report'].browse(res_id)
        data = {}
        if reportObj:
            resp = reportObj.get_report()
            data = {'embed_url':resp.get('embed_url'), 'embed_token':resp.get('embed_token'), 'token_expiry':resp.get('token_expiry')}
        return data

    @http.route("/get/dashboardparameter", auth="user", type="json")
    def get_dashboard_parameter(self, res_id, **kw):
        dashboardObj = request.env['powerbi.dashboard'].browse(res_id)
        data = {}
        if dashboardObj:
            resp = dashboardObj.get_dashboard()
            data = {'embed_url':resp.get('embed_url'), 'embed_token':resp.get('embed_token'), 'token_expiry':resp.get('token_expiry')}
        return data

    @http.route("/odoo_connect/instance/<int:instance_id>", type="http", auth="user")
    def odoo_connect(self, instance_id, **kw):
        connectionObj = request.env["powerbi.connection"].browse(instance_id)
        if connectionObj and kw.get('code'):
            connectionObj.state='connected'
            connectionObj.status = "Test connection successful, now you can proceed with synchronization!!"
            connectionObj.connection_status = True
        action_id = request.env.ref('odoo_powerbi_connect.powerbi_connection_tree_action').id
        url = f"/web#id={connectionObj.id}&action={action_id}&model=powerbi.connection&view_type=form"
        return request.redirect(url)
