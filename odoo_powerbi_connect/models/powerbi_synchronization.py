# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

import json
import requests
import datetime
import logging
from odoo.http import request
from odoo import models

_logger = logging.getLogger(__name__)

class PowerbiSynchronization(models.TransientModel):
    _name = "powerbi.synchronization"
    _description = "Power BI Synchronization"

    def defaultConvert(self, val):
        if isinstance(val, datetime.datetime) or isinstance(val, datetime.date):
            return str(val)

    def callPowerbiApi(self, url, method, data={}, token='', scope=[]):
        status, message = True, ''
        if not token:
            connection = self.env["powerbi.connection"].get_active_connection()._create_powerbi_connection(scope)
            if connection.get("status", False):
                token = connection.get("token")
            else:
                message = connection.get('message','')
                return {'status':False, 'message':message, 'value':{}}

        headers = {"Authorization": token, "Content-Type": "application/json"}
        try:
            user_agent = request.httprequest.environ.get('HTTP_USER_AGENT', '')
            headers["User-Agent"] = user_agent
        except Exception as e:
            _logger.debug("### User-Agent Exception - %r ",e)

        if method == "post":
            data = json.dumps(data, default=self.defaultConvert)
            resp = requests.post(url, headers=headers, data=data, verify=True)
        elif method == "put":
            data = json.dumps(data, default=self.defaultConvert)
            resp = requests.put(url, headers=headers, data=data, verify=True)
        elif method == "get":
            resp = requests.get(url, headers=headers, verify=True)
        elif method == "delete":
            resp = requests.delete(url, headers=headers, verify=True)
           
        else:
            return {'status':False, 'message':"Wrong method selected", 'value':{}}

        try:
            resp_val = json.loads(resp.text)
        except Exception as e:
            resp_val = str(e)
        if not resp.ok:
            status = False
            message = str(resp.reason or 'Error during API call')
        
        return {'status':status, 'message':message, 'value':resp_val}

    def get_embed_token(self, ttype, dataObj, connObj, scopes):
        if dataObj.workspace_id.default_workspace:
            url = f"{connObj.api_url}/GenerateToken"
            token_data = {
                "datasets": [
                    {"id": dataObj.dataset_id.powerbi_id}
                ],
                f'{ttype}' : [
                    {"id": dataObj.powerbi_id}
                ]
            }
        else:
            url = f"{connObj.api_url}/groups/{dataObj.workspace_id.powerbi_id}/{ttype}/{dataObj.powerbi_id}/GenerateToken"
            token_data = {
                "accessLevel": "View"
            }
        connection = connObj._create_powerbi_connection(scopes)
        resp = self.callPowerbiApi(url, "post", data=token_data, token=connection.get('token',''), scope=scopes)
        
        if resp.get('status'):
            value = resp.get('value')
            return {'token': value.get('token'), 'expiry': value.get('expiration')}
        else:
            message="Token generation error - "+str(resp.get("message",""))
            dataObj.message_post(body=message)
        return {}
