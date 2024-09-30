# Copyright © 2023 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging
from typing import List

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSaleTracking(WebsiteSale):

    @http.route(
        ['/shop/tracking_data'],
        type='json',
        auth="public",
        methods=['POST'],
        website=True,
        # csrf=False,
    )
    def tracking_event_data(
            self,
            event_type: str,
            item_type: str = 'product.template',
            product_ids: List[int] = None,
            product_qty: int = 1,
            order_id: int = None,
            **kw,
    ):
        """Pass data from JS to the method "_tracking_event_data"
        to get data to send to a tracing service.

        This controller is used to get the current website instance.

        :param event_type: one of the list "TRACKING_EVENT_TYPES' item
        :param item_type: can be 'product.template' or 'product.product'
        :param product_ids: list of record ID for the "product.product"
            or "product.template" model (depends on the param "item_type")
        :param product_qty: specify how much products was added to cart
        :param order_id: ID of a record of the "sale.order" model
        :param kw: optional additional params
        :return dict:
        """
        if item_type not in ['product.template', 'product.product']:
            return {'error': 'Item type "%s" is not supported.' % item_type}
        product_data = []
        pricelist = request.website.pricelist_id
        products = product_ids or []
        for product_id in products:
            p = request.env[item_type].browse(product_id)
            if item_type == 'product.template':
                price = p._get_combination_info(pricelist=pricelist)['price']
                product_template = p
                product_variant = p.product_variant_id
            else:
                price = p._get_combination_info_variant(pricelist=pricelist)['price']
                product_template = p.product_tmpl_id
                product_variant = p
            product_data.append({
                'product_tmpl_id': product_template.id,
                'product_id': product_variant.id,
                'qty': product_qty,
                'price': float("%.2f" % price),  # to remove trailing float zeros
            })

        request_env = request.httprequest.headers.environ
        request_data = {
            'user_agent': request.httprequest.user_agent.string,
            'ip': request_env.get("REMOTE_ADDR"),
            'visitor_uuid': request.httprequest.cookies.get('visitor_uuid', ''),
            'url': request.httprequest.referrer,
        }
        return request.website.with_context(kw).sudo()._tracking_event_data(
            event_type=event_type,
            product_data=product_data,
            pricelist_id=pricelist.id,
            order_id=order_id,
            request_data=request_data,
        )
