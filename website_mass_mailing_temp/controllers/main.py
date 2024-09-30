# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.http import route, request
from odoo.addons.website_mass_mailing.controllers.main import MassMailController


class MassMailControllerTemp(MassMailController):

    @route('/website_mass_mailing/is_subscriber', type='json', website=True, auth='public')
    def is_subscriber(self, list_id, subscription_type, **post):
        if not list_id:
            list_id = request.env['mailing.list'].sudo().search([('use_by_default', '=', True)], limit=1).id
        return super().is_subscriber(list_id=list_id, subscription_type=subscription_type, **post)

    @route('/website_mass_mailing/subscribe', type='json', website=True, auth='public')
    def subscribe(self, list_id, value, subscription_type, **post):
        if not list_id:
            list_id = request.env['mailing.list'].sudo().search([('use_by_default', '=', True)], limit=1).id
        return super().subscribe(list_id=list_id, value=value, subscription_type=subscription_type, **post)
