# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResPartnerTicket(models.Model):

    _inherit = "res.partner"

    support_ticket_ids = fields.One2many('website.support.ticket', 'partner_id', string="Tickets")
    support_ticket_count = fields.Integer(compute="_count_support_tickets", string="Ticket Count")
    new_support_ticket_count = fields.Integer(compute="_count_new_support_tickets", string="New Ticket Count")
    support_ticket_string = fields.Char(compute="_compute_support_ticket_string", string="Support Ticket String")
    sla_id = fields.Many2one('website.support.sla', string="SLA")
    dedicated_support_user_id = fields.Many2one('res.users', string="Dedicated Support User")

    # @api.one
    @api.depends('support_ticket_ids')
    def _count_support_tickets(self):
        """Sets the amount support tickets owned by this customer"""
        for rec in self:
            rec.support_ticket_count = rec.support_ticket_ids.search_count([('partner_id','=',rec.id)])

    # @api.one
    @api.depends('support_ticket_ids')
    def _count_new_support_tickets(self):
        """Sets the amount of new support tickets owned by this customer"""
        for rec in self:
            opened_state = self.env['ir.model.data'].get_object('website_support', 'website_ticket_state_open')
            rec.new_support_ticket_count = rec.support_ticket_ids.search_count([('partner_id','=',rec.id), ('state_id','=',opened_state.id)])

    # @api.one
    @api.depends('support_ticket_count', 'new_support_ticket_count')
    def _compute_support_ticket_string(self):
        for rec in self:
            rec.support_ticket_string = str(rec.support_ticket_count) + " (" + str(rec.new_support_ticket_count) + ")"
