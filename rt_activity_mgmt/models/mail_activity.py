# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]


class MailActivity(models.Model):
    _inherit = "mail.activity"

    rt_activity_mgmt_color = fields.Integer('Color Index', default=0)
    rt_activity_mgmt_priority = fields.Selection(
        AVAILABLE_PRIORITIES, string='Priority', index=True,
        default=AVAILABLE_PRIORITIES[0][0])

    rt_activity_mgmt_tag_ids = fields.Many2many(
        comodel_name='rt_activity_mgmt.mail.activity.tag', relation='rt_activity_mgmt_activity_tag_rel', string='Tags',
    )

    def action_rt_activity_mgmt_activity_edit(self):
        self.ensure_one()
        return {
            'name': self.display_name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.activity',
            'res_id': self.id,
            'target': 'new',
        }

    def action_rt_activity_mgmt_activity_document(self):            
        self.ensure_one()
        if self.res_id and self.res_model:
            return {
                'res_id': self.res_id,
                'res_model': self.res_model,
                'target': 'current',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
            }
                
            # domain = [['id', '=', self.res_id]]
            # return {
            #     'type': 'ir.actions.act_window',
            #     'name': self.res_model_id.sudo().name if self.res_model_id else '',
            #     'res_model': self.res_model,
            #     'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
            #     'search_view_id': [False],
            #     'domain': domain,
            # }
        else:
            raise ValidationError(
                _('Document model or document id does not exist!'))

    @api.model
    def rt_activity_mgmt_retrieve_dashboard(self, domain=[]):
        """ This function returns the values to populate the custom dashboard in
            the activity views.
        """
        self.check_access_rights('read')

        result = {
            'all_state_overdue': 0,
            'all_state_today': 0,
            'all_state_planned': 0,
            'list_overview_activity_type': [],
        }

        activities = self.env['mail.activity'].search(domain)

        today = fields.Date.context_today(self)
        result['all_state_overdue'] = len(
            activities.filtered(lambda a: a.date_deadline < today).ids)
        result['all_state_today'] = len(activities.filtered(
            lambda a: a.date_deadline == today).ids)
        result['all_state_planned'] = len(
            activities.filtered(lambda a: a.date_deadline > today).ids)

        activity_type_ids = activities.mapped('activity_type_id')
        list_overview_activity_type = []
        if activity_type_ids:
            for activity_type_id in activity_type_ids:
                dic_activity_type_overview = {
                    'activity_type_name': activity_type_id.name,
                    'overdue': len(activities.filtered(lambda a: a.date_deadline < today and a.activity_type_id == activity_type_id).ids),
                    'today': len(activities.filtered(lambda a: a.date_deadline == today and a.activity_type_id == activity_type_id).ids),
                    'planned': len(activities.filtered(lambda a: a.date_deadline > today and a.activity_type_id == activity_type_id).ids),
                }
                list_overview_activity_type.append(dic_activity_type_overview)
        result['list_overview_activity_type'] = list_overview_activity_type
        return result
