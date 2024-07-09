# -*- coding: utf-8 -*-


from odoo import fields, api, models, _


class Message(models.Model):
    _inherit = 'mail.message'

    @api.model
    def rt_activity_mgmt_action_view_mail_message(self):
        domain = [('subtype_id', '=', self.env['ir.model.data']._xmlid_to_res_id(
            'mail.mt_activities'))]
        if not self.env.user.has_group('rt_activity_mgmt.rt_activity_mgmt_group_mail_activity_manager'):
            domain.append(('author_id', '=', self.env.user.partner_id.id))

        return {
            'view_mode': 'tree',
            'name': _('Done Activity Logs'),
            'res_model': 'mail.message',
            'type': 'ir.actions.act_window',
            'domain': domain,
            'search_view_id': [self.env.ref('rt_activity_mgmt.view_message_search').id, 'search'],
            'views': [
                [self.env.ref('rt_activity_mgmt.view_message_tree').id, 'list'], 
                [self.env.ref('rt_activity_mgmt.mail_message_view_form').id, 'form'],
                [self.env.ref('rt_activity_mgmt.view_message_kanban').id, 'kanban'],
                [self.env.ref('rt_activity_mgmt.view_message_calendar').id, 'calendar'],
                [self.env.ref('rt_activity_mgmt.view_message_pivot').id, 'pivot'],
                [self.env.ref('rt_activity_mgmt.view_message_graph').id, 'graph'],                
                ],
        }
