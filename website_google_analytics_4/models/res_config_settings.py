# Copyright © 2021 Garazd Creation (<https://garazd.biz>)

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ga4_debug_mode = fields.Boolean(
        related='website_id.ga4_debug_mode',
        readonly=False,
    )
    ga4_tracking_key = fields.Char(
        related='website_id.ga4_tracking_key',
        readonly=False,
    )

    @api.depends('website_id')
    def has_google_analytics_4(self):
        self.has_google_analytics_4 = bool(self.ga4_tracking_key)

    def inverse_has_google_analytics_4(self):
        if not self.has_google_analytics_4:
            self.ga4_tracking_key = False

    has_google_analytics_4 = fields.Boolean(
        string='Google Analytics 4',
        compute=has_google_analytics_4,
        inverse=inverse_has_google_analytics_4,
    )
