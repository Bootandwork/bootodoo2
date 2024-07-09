# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class ActivityTag(models.Model):
    _name = "rt_activity_mgmt.mail.activity.tag"
    _description = "Activity Tag"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color', default=_get_default_color)

    @api.constrains('name')
    def _check_name_constraint(self):
        """ name must be unique """
        for tag in self.filtered(lambda t: t.name):
            domain = [('id', '!=', tag.id), ('name', '=', tag.name)]
            if self.search(domain):
                raise ValidationError(_('Tag name already exists !'))
