# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

import json
from odoo import fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from datetime import timedelta
from babel.dates import format_date, format_datetime

class PowerbiConnectorDashboard(models.Model):
    _name = "powerbi.connector.dashboard"
    _description = "PowerBI Connector Dashboard"

    color = fields.Integer(string='Color Index',default=6)
    name = fields.Char(string="Name",default='abhi')
    state = fields.Selection(
        [('dataset', 'Dataset'), ('workspace', 'Workspace'), ('report', 'Report'), ('table', 'Table'),('dashboard', 'Dashboard')])
    total_count=fields.Integer(compute="_total_count")
    publish_count=fields.Integer(compute="_publish_count")
    unpublish_count=fields.Integer(compute="_unpublish_count")
    count_mapped_records = fields.Integer(compute='_compute_record_count')
    kanban_dashboard_graph_data = fields.Text(compute='_kanban_dashboard_graph_data')

    '''This method Used To Redirect Total Data Of selected Models '''
    def total_data(self):
       for rec in self:
            if rec.state=="dataset":
                model_name='powerbi.dataset'
            if rec.state=="workspace":
                model_name='powerbi.workspace'
            if rec.state=="table":
                model_name='powerbi.table'
            if rec.state=="report":
                model_name='powerbi.report'
            if rec.state=="dashboard":
                model_name='powerbi.dashboard'
            return {
                "type":"ir.actions.act_window",
                'name':rec.name,
                'res_model':model_name,
                'view_mode':'tree,form',
                'target':'current'
            }
  
    '''This method Used To Count Total Data Of Models '''
    def _total_count(self):
        for rec in self:
            if rec.state=='dataset':
                record=self.env['powerbi.dataset'].search([]).ids
                rec.total_count=len(record)
            if rec.state=='workspace':
                record=self.env['powerbi.workspace'].search([]).ids
                rec.total_count=len(record)

            if rec.state=='table':
                record=self.env['powerbi.table'].search([]).ids
                rec.total_count=len(record)
            
            if rec.state=='report':
                record=self.env['powerbi.report'].search([]).ids
                rec.total_count=len(record)

            if rec.state=='dashboard':
                record=self.env['powerbi.dashboard'].search([]).ids
                rec.total_count=len(record)

    '''This method Used To Count Total Publish Data Models '''
    def _publish_count(self):
        for rec in self:
            if rec.state=='dataset':
                record=self.env['powerbi.dataset'].search([('is_published','=',True)]).ids
                rec.publish_count=len(record)
            if rec.state=='workspace':
                record=self.env['powerbi.workspace'].search([('is_published','=',True)]).ids
                rec.publish_count=len(record)

            if rec.state=='table':
                record=self.env['powerbi.table'].search([('is_published','=',True)]).ids
                rec.publish_count=len(record)
            
            if rec.state=='report':
                rec.publish_count=0
            
            if rec.state=='dashboard':
                rec.publish_count=0

    '''This method Used To Count Total UnPublish Data Models '''
    def _unpublish_count(self):
        for rec in self:
            if rec.state=='dataset':
                record=self.env['powerbi.dataset'].search([('is_published','=',False)]).ids
                rec.unpublish_count=len(record)
            if rec.state=='workspace':
                record=self.env['powerbi.workspace'].search([('is_published','=',False)]).ids
                rec.unpublish_count=len(record)

            if rec.state=='table':
                record=self.env['powerbi.table'].search([('is_published','=',False)]).ids
                rec.unpublish_count=len(record)
            
            if rec.state=='report':
                rec.unpublish_count=0

            if rec.state=='dashboard':
                rec.unpublish_count=0


    '''This method Used To Redirect Unpublish Data Of selected Models '''
    def action_unpublish(self):
       for rec in self:
            if rec.state=="dataset":
                model_name='powerbi.dataset'
            if rec.state=="workspace":
                model_name='powerbi.workspace'
            if rec.state=="table":
                model_name='powerbi.table'
            if rec.state=="report":
                model_name='powerbi.report'
            if rec.state=="dashboard":
                model_name='powerbi.dashboard'
            return {
                "type":"ir.actions.act_window",
                'name':rec.name,
                'res_model':model_name,
                'domain':[('is_published','=',False)],
                'view_mode':'tree,form',
                'target':'current'
                }
    
    '''This method Used To Redirect Publish Data Of selected Models '''
    def action_publish(self):
        for rec in self:
            if rec.state=="dataset":
                model_name='powerbi.dataset'
            if rec.state=="workspace":
                model_name='powerbi.workspace'
            if rec.state=="table":
                model_name='powerbi.table'
            if rec.state=="report":
                model_name='powerbi.report'
            if rec.state=="dashboard":
                model_name='powerbi.dashboard'
            return {
                "type":"ir.actions.act_window",
                'name':rec.name,
                'res_model':model_name,
                'domain':[('is_published','=',True)],
                'view_mode':'tree,form',
                'target':'current'
                }
    
    def _kanban_dashboard_graph_data(self):
        for record in self:
            if record.state=='workspace':
                record.kanban_dashboard_graph_data = json.dumps(
                    record.get_bar_graph_datas('powerbi_workspace'))
            if record.state=='dataset':
                record.kanban_dashboard_graph_data = json.dumps(
                    record.get_bar_graph_datas('powerbi_dataset'))
            if record.state=='table':
                record.kanban_dashboard_graph_data = json.dumps(
                    record.get_bar_graph_datas('powerbi_table'))
            if record.state=='report':
                record.kanban_dashboard_graph_data = json.dumps(
                    record.get_bar_graph_datas('powerbi_report'))
            if record.state=='dashboard':
                record.kanban_dashboard_graph_data = json.dumps(
                    record.get_bar_graph_datas('powerbi_dashboard'))
    
    def get_bar_graph_datas(self,modelName):
        self.ensure_one()
        fecthDate = 'create_date'
        data = []
        today = fields.Date.context_today(self)
        data.append({'label': _('Past'), 'value': 0.0})
        day_of_week = int(
            format_datetime(
                today,
                'e',
                locale=self._context.get(
                    'lang',
                    'en_US')))
        first_day_of_week = today + timedelta(days=-day_of_week + 1)
        for i in range(-1, 1):
            if i == 0:
                label = _('This Week')
            else:
                start_week = first_day_of_week + timedelta(days=i * 7)
                end_week = start_week + timedelta(days=6)
                if start_week.month == end_week.month:
                    label = str(start_week.day) + '-' + str(end_week.day) + ' ' + format_date(
                        end_week, 'MMM', locale=self._context.get('lang', 'en_US'))
                else:
                    label = format_date(start_week, 'd MMM', locale=self._context.get('lang', 'en_US')) \
                        + '-' \
                        + format_date(end_week, 'd MMM', locale=self._context.get('lang', 'en_US'))
            data.append({'label': label, 'value': 0.0})

        # Build SQL query to find amount aggregated by week
        select_sql_clause ="""SELECT COUNT(*) as total FROM """+modelName
        
        query = ''
        start_date = (first_day_of_week + timedelta(days=-7))
        for i in range(0, 3):
            if i == 0:
                query += "(" + (select_sql_clause) + " where " + \
                    fecthDate + " < '" + start_date.strftime(DF) + "')"
            else:
                next_date = start_date + timedelta(days=7)
                query += " UNION ALL (" + (select_sql_clause) + " where " + fecthDate + " >= '" + start_date.strftime(
                    DF) + "' and " + fecthDate + " < '" + next_date.strftime(DF) + "')"
                start_date = next_date

        self.env.cr.execute(query)
        query_results = self.env.cr.dictfetchall()
        for index in range(0, len(query_results)):
            total = str(query_results[index].get('total'))
            total = total.split('L')
            if int(total[0]) > 0:
                data[index]['value'] = total[0]

        color = '#3e1e5e'
        graphData = [{'values': data, 'area': True, 'title': '', 'key': modelName, 'color': color}]
        return graphData
