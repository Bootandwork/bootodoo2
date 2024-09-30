# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.


from odoo import models


class ThemeNew(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_crafito_post_copy(self, mod):
        self.disable_view('website_theme_install.customize_modal')
