# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Kinfinity Tech Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class WebsiteOneSignal(models.Model):
    _inherit = 'website'

    onesignalsdk_app_id = fields.Char(
        string='App Id')
    onesignalsdk_safari_web_id = fields.Char(
        string='Safari Web Id')


class WebsiteConfigSettingsOneSignal(models.TransientModel):
    _inherit = 'res.config.settings'

    onesignalsdk_app_id = fields.Char(
        related='website_id.onesignalsdk_app_id')
    onesignalsdk_safari_web_id = fields.Char(
        related='website_id.onesignalsdk_safari_web_id')
