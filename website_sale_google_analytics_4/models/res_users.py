import uuid

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _default_ga4_ref(self):
        return str(uuid.uuid4())

    ga4_ref = fields.Char(
        string='GA4 User ID',
        default=_default_ga4_ref,
        readonly=True,
        copy=False,
    )

    @api.model
    def generate_ga4_ref(self):
        """Initial setting of a GA4 User-ID for portal and internal users."""
        for user in self.with_context(active_test=False).search([('ga4_ref', '=', False)]):
            user.ga4_ref = self._default_ga4_ref()
