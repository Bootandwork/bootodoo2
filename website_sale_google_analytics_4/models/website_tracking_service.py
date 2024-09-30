# Copyright © 2023 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class WebsiteTrackingService(models.Model):
    _inherit = "website.tracking.service"

    type = fields.Selection(
        selection_add=[('ga4', 'Google Analytics 4')],
        ondelete={'ga4': 'cascade'},
    )
    ga4_debug_mode = fields.Boolean(string='Debug Mode')
    ga4_lead_value = fields.Float(string='Lead Value', default=1.0)

    # flake8: noqa: E501
    @api.constrains('type', 'track_id_external', 'track_ip_address', 'track_user_agent',
                    'track_email', 'track_phone', 'track_country', 'track_city')
    def _check_available_visitor_data(self):
        super(WebsiteTrackingService, self)._check_available_visitor_data()
        for service in self.filtered(lambda s: s.type == 'ga4'):
            if any(service[track_option] for track_option in [
                'track_ip_address', 'track_user_agent',
                'track_email', 'track_phone', 'track_country', 'track_city',
            ]):
                raise ValidationError(
                    _('Only the following data can be sent to GA4: '
                      'External ID.')
                )

    def get_item_categories(self, product, property_name: str = 'content_category'):
        self.ensure_one()
        if self.type != 'ga4':
            return super(WebsiteTrackingService, self).get_item_categories(product, property_name)
        res = {}
        if self.category_type == 'product':
            res.update({'item_category': product.categ_id.name})
        elif self.category_type == 'public':
            category = product.public_categ_ids and product.public_categ_ids[:1] or None
            if category:
                for index, category in enumerate(category.parents_and_self[:5]):
                    res.update({'item_category%s' % ((index + 1) if index > 0 else ''): category.name})
            else:
                res.update({'item_category': '-'})
        return res

    def get_common_data(self, event_type, product_data_list, order, pricelist):
        self.ensure_one()
        if self.type != 'ga4':
            return super(WebsiteTrackingService, self).get_common_data(
                event_type=event_type,
                product_data_list=product_data_list,
                order=order,
                pricelist=pricelist,
            )
        currency = self.website_id._tracking_get_currency(order=order, pricelist=pricelist)
        data = {
            'send_to': self.key,
            'currency': currency.name,
        }
        return data

    def get_item_data_from_product_list(self, product_data_list, pricelist):
        self.ensure_one()
        if self.type != 'ga4':
            return super(WebsiteTrackingService, self).get_item_data_from_product_list(
                product_data_list=product_data_list,
                pricelist=pricelist,
            )
        service = self
        website = service.website_id
        currency = website._tracking_get_currency(pricelist=pricelist)

        items = []
        total_value = 0
        for product_data in product_data_list:
            product = service.get_item(product_data)
            price = product_data.get('price', 0)
            total_value += price
            item_data = {
                'item_id': '%d' % product.id,
                'item_name': product.name,
                'price': float('%.2f' % price),
                'currency': currency.name,
                'quantity': product_data.get('qty', 1),
            }
            item_data.update(service.get_item_categories(product))
            items.append(item_data)
        return {
            'value': float('%.2f' % total_value),
            'items': items,
        }

    def get_item_data_from_order(self, order):
        self.ensure_one()
        if self.type != 'ga4':
            return super(WebsiteTrackingService, self).get_item_data_from_order(order)
        service = self
        items = []
        for line in order.order_line:

            product = line.product_id
            if service.item_type == 'product.template':
                product = product.product_tmpl_id

            item_data = {
                'item_id': '%d' % product.id,
                'item_name': product.name,
                'price': float('%.2f' % service._get_final_product_price(line)),
                'currency': order.pricelist_id.currency_id.name,
                'quantity': line.product_uom_qty,
            }
            item_data.update(service.get_item_categories(product))
            items.append(item_data)
        items_data = {
            'items': items,
            'value': float('%.2f' % order.amount_total),
        }
        return items_data

    def get_data_for_lead(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        if self.type == 'ga4':
            return {'value': self.ga4_lead_value}
        return super(WebsiteTrackingService, self).get_data_for_lead(product_data_list, pricelist, order)

    def get_data_for_login(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        if self.type == 'ga4':
            return {'method': 'Odoo'}
        return super(WebsiteTrackingService, self).get_data_for_login(product_data_list, pricelist, order)

    def get_data_for_sign_up(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        if self.type == 'ga4':
            return {'method': 'Odoo'}
        return super(WebsiteTrackingService, self).get_data_for_sign_up(product_data_list, pricelist, order)

    def get_data_for_search_product(self, product_data_list, pricelist, order):
        self.ensure_one()
        if self.type != 'ga4':
            return super(WebsiteTrackingService, self).get_data_for_search_product(
                product_data_list=product_data_list,
                pricelist=pricelist,
                order=order,
            )
        data = {}
        search_term = self._context.get('search_term', '')
        data.update({'search_term': search_term})
        return data

    def get_data_for_purchase(self, product_data_list, pricelist, order):
        self.ensure_one()
        data = super(WebsiteTrackingService, self).get_data_for_begin_checkout(
            product_data_list=product_data_list,
            pricelist=pricelist,
            order=order,
        )
        if self.type == 'ga4':
            data.update({
                'transaction_id': order.name,
                'tax': order.amount_tax,
            })
        return data

    @api.model
    def _get_privacy_url(self):
        urls = super(WebsiteTrackingService, self)._get_privacy_url()
        urls.update({'ga4': 'https://developers.google.com/analytics/devguides/collection/protocol/ga4/policy'})
        return urls

    @api.model
    def _fields_to_invalidate_cache(self):
        res = super(WebsiteTrackingService, self)._fields_to_invalidate_cache()
        res += ['ga4_debug_mode', 'track_id_external']
        return res
