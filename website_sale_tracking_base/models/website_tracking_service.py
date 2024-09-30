# Copyright © 2023 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

from typing import Dict, List

from odoo import _, api, fields, models
from odoo.http import request


class WebsiteTrackingService(models.Model):
    _name = "website.tracking.service"
    _inherit = ['mail.thread']
    _description = 'Service that gets Tracking Event Data'
    _order = 'sequence, website_id, type'

    def _default_website(self):
        return self.env['website'].search([('company_id', '=', self.env.company.id)], limit=1)  # flake8: noqa: E501

    # flake8: noqa: E501
    type = fields.Selection(selection=[])
    key = fields.Char(tracking=True)
    key_is_required = fields.Boolean(default=True, tracking=True)
    cookie_type = fields.Selection(selection=[])
    website_id = fields.Many2one(
        comodel_name='website',
        ondelete='cascade',
        default=_default_website,
        required=True,
    )
    item_type = fields.Selection(
        selection=[
            ('product.template', 'Product Template ID'),
            ('product.product', 'Product ID'),
        ],
        default='product.template',
        required=True,
    )
    category_type = fields.Selection(
        selection=[
            ('public', 'Public Category (with hierarchy)'),
            ('product', 'Product Category'),
        ],
        default='public',
        required=True,
    )
    is_internal_logged = fields.Boolean(string="Internal Logs", tracking=True)
    sequence = fields.Integer(default=100)
    active = fields.Boolean(default=True, tracking=True)
    # Advanced Matching
    privacy_url = fields.Char(string='Data Use Privacy URL', readonly=True)
    track_id_external = fields.Boolean(string="Track External ID", tracking=True)
    track_ip_address = fields.Boolean(string="Track IP Address", tracking=True)
    track_user_agent = fields.Boolean(string="Track User Agent", tracking=True)
    track_email = fields.Boolean(string="Track Email", tracking=True)
    track_phone = fields.Boolean(string="Track Phone", tracking=True)
    track_country = fields.Boolean(string="Track Country", tracking=True)
    track_city = fields.Boolean(string="Track City", tracking=True)
    lead_value = fields.Float(default=1.0, help="A lead value for the Contact Us form.")
    show_lead_value = fields.Boolean(compute='_compute_show_lead_value')

    @api.constrains('type', 'track_id_external', 'track_ip_address', 'track_user_agent',
                    'track_email', 'track_phone', 'track_country', 'track_city')
    def _check_available_visitor_data(self):
        """Define what website visitor data can be activated in a service.
        Method to override."""
        pass

    @api.depends('type')
    def _compute_show_lead_value(self):
        for service in self:
            service.show_lead_value = 'lead' in self.env['website']._tracking_event_mapping(service.type).keys()

    def name_get(self):
        return [(rec.id, "%s%s" % (
            dict(self._fields['type'].selection).get(rec.type),
            rec.key and f": {rec.key}" or '',
        )) for rec in self]

    def allow_send_data(self):
        """Method to check additional restrictions. To override."""
        self.ensure_one()
        return self.active and self.key

    def get_item(self, item_data):
        self.ensure_one()
        service = self
        template_id = item_data.get('product_tmpl_id')
        variant_id = item_data.get('product_id')
        if service.item_type == 'product.template':
            product = self.env['product.template'].browse(template_id)
        elif service.item_type == 'product.product':
            product = self.env['product.product'].browse(variant_id)
        else:
            product = None
        return product

    def get_item_categories(self, product, property_name: str = 'content_category') -> Dict:
        """Generate a product category hierarchy structure.
        :param product: a record of the "product.product" model
        """
        self.ensure_one()
        res = {}
        if self.category_type == 'product':
            res.update({property_name: product.categ_id.name})
        elif self.category_type == 'public':
            # Use the first public category of a product
            if product.public_categ_ids[:1]:
                category = product.public_categ_ids[:1].name
            else:
                category = _('All products')
            res.update({property_name: category})
        return res

    def get_common_data(self, event_type, product_data_list=None, order=None, pricelist=None):
        self.ensure_one()
        return {}

    def get_item_data_from_product_list(self, product_data_list, pricelist) -> Dict:
        """Prepare data for a tracking service from a product data list.
        :param product_data_list: a list with product data (take a look at "controllers/main.py")
        :param pricelist: a record of the model "product.pricelist"
        """
        self.ensure_one()
        return {}

    def get_item_data_from_order(self, order) -> Dict:
        """Prepare data for a tracking service from a sale order.
        :param order: a record of the model "sale.order"
        """
        self.ensure_one()
        return {}

    def _get_final_product_price(self, order_line) -> float:
        self.ensure_one()
        if self.env.user.has_group('account.group_show_line_subtotals_tax_excluded'):
            price = order_line.price_reduce_taxexcl
        elif self.env.user.has_group('account.group_show_line_subtotals_tax_included'):
            price = order_line.price_reduce_taxinc
        else:
            price = order_line.price_unit
        return price

    def get_data_for_lead(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        return {'value': self.lead_value}

    def get_data_for_login(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        return {}

    def get_data_for_sign_up(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        return {}

    def get_data_for_view_product_list(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        return self.get_item_data_from_product_list(product_data_list, pricelist)

    def get_data_for_view_product_category(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        return self.get_item_data_from_product_list(product_data_list, pricelist)

    def get_data_for_search_product(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        return self.get_item_data_from_product_list(product_data_list, pricelist)

    def get_data_for_view_product(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        return self.get_item_data_from_product_list(product_data_list, pricelist)

    def get_data_for_add_to_wishlist(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        return self.get_item_data_from_product_list(product_data_list, pricelist)

    def get_data_for_add_to_cart(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        return self.get_item_data_from_product_list(product_data_list, pricelist)

    def get_data_for_begin_checkout(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        return self.get_item_data_from_order(order)

    def get_data_for_add_shipping_info(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        return self.get_item_data_from_order(order)

    def get_data_for_add_payment_info(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        return self.get_item_data_from_order(order)

    def get_data_for_purchase(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        return self.get_item_data_from_order(order)

    def get_data_for_purchase_portal(self, product_data_list=None, pricelist=None, order=None):
        self.ensure_one()
        return self.get_item_data_from_order(order)

    def get_visitor_data(self) -> Dict:
        self.ensure_one()
        visitor_data = {}

        if not request:
            return visitor_data
        visitor = self.env['website.visitor']._get_visitor_from_request(force_create=False)  # flake8: noqa: E501
        if not visitor:
            return visitor_data

        service = self
        log = self.env['website.tracking.log']

        if service.track_id_external:
            visitor_data["external_id"] = visitor.access_token

        country = visitor.partner_id.country_id or visitor.country_id
        if service.track_country and country:
            visitor_data["country"] = log._hash_sha256(country.name)

        if service.track_city and visitor.partner_id.city:
            visitor_data["ct"] = log._hash_sha256(visitor.partner_id.city)

        if service.track_email and visitor.email:
            visitor_data["em"] = log._hash_email(visitor.email)

        phone = visitor.partner_id and (
            visitor.partner_id.phone or visitor.partner_id.mobile) or visitor.mobile
        if service.track_phone and phone and country:
            remove_plus = self._context.get('phone_remove_plus', True)
            visitor_data["ph"] = log._hash_phone_number(phone, country, remove_plus=remove_plus)
        return visitor_data

    @api.model
    def _get_privacy_url(self) -> Dict:
        return {}

    @api.model
    def _fields_to_invalidate_cache(self) -> List[str]:
        return ['sequence', 'website_id', 'key', 'active']

    @api.model_create_multi
    def create(self, vals_list):
        # Set up a default privacy URL for a tracking services
        for vals in vals_list:
            service_type = vals.get('type')
            if service_type and self._get_privacy_url().get(service_type):
                vals['privacy_url'] = self._get_privacy_url().get(service_type)
        record = super(WebsiteTrackingService, self).create(vals_list)
        # Invalidate the caches to apply changes on webpages
        self.env['ir.qweb'].clear_caches()
        return record

    def write(self, vals):
        result = super(WebsiteTrackingService, self).write(vals)
        if any(fld in vals for fld in self._fields_to_invalidate_cache()):
            # Invalidate the caches to apply changes on webpages
            self.env['ir.qweb'].clear_caches()
        return result

    def extra_log_data(self):
        """Add extra values on to the "log" record. Method to override."""
        self.ensure_one()
        return {}

    def post_processed_data(self, event_data: Dict) -> Dict:
        """Perform post-processing of event data. Return a dictionary to update.
           Method to override.
        """
        self.ensure_one()
        return {}
