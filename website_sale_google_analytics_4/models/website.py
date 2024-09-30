# Copyright © 2023 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html).

import logging

from odoo import api, models
from odoo.http import request

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = "website"

    @api.model
    def _tracking_event_mapping(self, service_type):
        res = super(Website, self)._tracking_event_mapping(service_type)
        if service_type == 'ga4':
            res = {
                'lead': 'generate_lead',
                'login': 'login',
                'sign_up': 'sign_up',
                'view_product': 'view_item',
                'view_product_list': 'view_item_list',
                'search_product': 'search',
                'add_to_wishlist': 'add_to_wishlist',
                'add_to_cart': 'add_to_cart',
                'begin_checkout': 'begin_checkout',
                'add_shipping_info': 'add_shipping_info',
                'add_payment_info': 'add_payment_info',
                'purchase': 'purchase',
                'purchase_portal': 'purchase',
            }
        return res

    def _ga4_params(self):
        # flake8: noqa: E501
        """The method is completely overridden to get params related to tracking services."""
        super(Website, self)._ga4_params()
        params = {}
        service = self.env['website.tracking.service'].sudo().browse(self._context.get('tracking_service_id'))
        if service and service.ga4_debug_mode:
            params.update({'debug_mode': True})
        if service and service.track_id_external and request and request.env.user.has_group('base.group_portal') and request.env.user.ga4_ref:
            # Send "User-ID" only for portal users
            params.update({'user_id': request.env.user.ga4_ref})
        return params

    def _ga4_configs(self):
        super(Website, self)._ga4_configs()
        configs = []
        for service in self.sudo().tracking_service_ids.filtered(
                lambda s: s.type == 'ga4' and s.active
        ):
            configs.append({
                'key': service.key,
                'params':
                self.with_context(tracking_service_id=service.id)._ga4_params(),
            })
        return configs

    def ga4_get_primary_key(self):
        super(Website, self).ga4_get_primary_key()
        primary_service = self.sudo().tracking_service_ids.filtered(
            lambda s: s.type == 'ga4' and s.active
        )
        return primary_service and primary_service[0].key or ''
