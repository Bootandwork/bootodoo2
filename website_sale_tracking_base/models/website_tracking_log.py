# Copyright © 2023 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import json
from datetime import datetime
from hashlib import sha256

from odoo import api, fields, models
from odoo.addons.phone_validation.tools import phone_validation
from odoo.addons.base.models.res_country import Country
from .website import TRACKING_EVENT_TYPES


class WebsiteTrackingLog(models.Model):
    _name = "website.tracking.log"
    _description = 'Website Tracking Event Logs'
    _order = 'create_date DESC'

    service_id = fields.Many2one(
        comodel_name='website.tracking.service',
        ondelete='cascade',
        required=True,
    )
    website_id = fields.Many2one(
        related='service_id.website_id',
        store=True,
    )
    service_type = fields.Selection(
        related='service_id.type',
        store=True,
    )
    event_type = fields.Selection(
        selection=TRACKING_EVENT_TYPES,
        required=True,
    )
    payload = fields.Char(readonly=True)
    payload_preview = fields.Char(compute='_compute_payload_preview')
    product_ids = fields.Many2many(
        comodel_name='product.product',
        string='Products',
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        compute='_compute_product_id',
        store=True,
    )
    order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Order',
        ondelete='cascade',
    )
    url = fields.Char(string='URL')
    visitor_id = fields.Many2one(comodel_name='website.visitor', ondelete='set null')
    search_term = fields.Char()
    # API related fields
    channel = fields.Selection(
        selection=[('js_script', 'JS Script')],
        string='Data Channel',
        default='js_script',
    )
    state = fields.Selection(
        selection=[
            ('to_send', 'To Send'),
            ('sent', 'Sent'),
            ('error', 'Error'),
        ],
    )
    api_response = fields.Char(string='API Response')
    api_sent_date = fields.Datetime(string='API Sent Date')
    # Website visitor's data
    user_agent = fields.Char()
    user_ip_address = fields.Char()

    @api.depends('payload')
    def _compute_payload_preview(self):
        for log in self:
            try:
                log.payload_preview = json.dumps(json.loads(log.payload), indent=2)
            except:
                log.payload_preview = ''

    @api.depends('product_ids')
    def _compute_product_id(self):
        for log in self:
            if log.product_ids and len(log.product_ids) == 1:
                log.product_id = log.product_ids[0].id
            else:
                log.product_id = False

    @api.model
    def _hash_sha256(self, value: str):
        return sha256(value.encode('utf-8')).hexdigest()

    @api.model
    def _to_unix_time(self, date_value: datetime):
        return round(date_value.timestamp())

    @api.model
    def _hash_email(self, email: str) -> str:
        return self._hash_sha256(email.lower())

    @api.model
    def _hash_phone_number(self, number: str, country: Country, remove_plus: bool = False) -> str:
        res = ''
        if country and number:
            phone_number = phone_validation.phone_format(
                number,
                country_code=country.code,
                country_phone_code=country.phone_code,
                force_format='E164',
                raise_exception=False,
            )
            if remove_plus:
                phone_number = phone_number.replace('+', '')
            res = self._hash_sha256(phone_number)
        return res

    def name_get(self):
        return [(rec.id, "%s (%s)" % (
            rec.service_id.display_name, rec.event_type
        )) for rec in self]

    def action_send_event(self):
        """Method to send request via API. To override."""
        self.ensure_one()
