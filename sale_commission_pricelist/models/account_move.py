# Copyright 2018 Tecnativa - Carlos Dauden <carlos.dauden@tecnativa.com>
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_commission_from_pricelist(self):
        self.ensure_one()
        pricelist_id = self.mapped('sale_line_ids').mapped('order_id').mapped('pricelist_id')
        if not pricelist_id:
            pricelist_id = self.partner_id.property_product_pricelist
        if not self.product_id or not pricelist_id:
            return False  # pragma: no cover
        rule_id = pricelist_id._get_product_rule(
            product=self.product_id,
            quantity=self.quantity or 1.0,
            uom=self.product_uom_id,
            date=self.date
        )
        rule = self.env["product.pricelist.item"].browse(rule_id)
        return rule.commission_id

    @api.depends("move_id.partner_id")
    def _compute_agent_ids(self):
        super(AccountMoveLine, self)._compute_agent_ids()
        for record in self:
            commission = record._get_commission_from_pricelist()
            if record.agent_ids and commission:
                record.agent_ids.update({"commission_id": commission.id})

    def _prepare_agent_vals(self, agent):
        self.ensure_one()
        res = super(AccountMoveLine, self)._prepare_agent_vals(agent)
        commission = self._get_commission_from_pricelist()
        if commission:
            res["commission_id"] = commission.id
        return res
