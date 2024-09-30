# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class MailingList(models.Model):
    _inherit = "mailing.list"

    use_by_default = fields.Boolean(
        string="Default?"
    )
