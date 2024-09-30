# Copyright 2023-TODAY Rapsodoo Iberia S.r.L. (www.rapsodoo.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api, _

READONLY_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'done', 'cancel'}
}


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_order = fields.Datetime(
        string="Order Date",
        required=True, readonly=False, copy=False,
        states=READONLY_FIELD_STATES,
        help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.",
        default=fields.Datetime.now)


