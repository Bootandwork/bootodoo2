# -*- coding: utf-8 -*-
# Part of Aselcis. See LICENSE file for full copyright and licensing details.
from odoo import api, models
from odoo.addons.http_routing.models.ir_http import url_for
from werkzeug import urls


class Slides(models.Model):
    _inherit = 'slide.slide'

    @api.depends('document_id', 'slide_type', 'mime_type')
    def _compute_embed_code(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if base_url[-1] == '/':
            base_url = base_url[:-1]
        for record in self:
            if record.datas and (not record.document_id or record.slide_type in ['document', 'presentation']):
                slide_url = base_url + url_for('/slides/embed/%s?page=1' % record.id)
                record.embed_code = '<iframe src="%s" class="o_wslides_iframe_viewer" allowFullScreen="true" height="%s" width="%s" frameborder="0"></iframe>' % (slide_url, 315, 420)
            elif record.slide_type == 'video' and record.document_id:
                if not record.mime_type:
                    # embed youtube video
                    query = urls.url_parse(record.url).query
                    query = query + '&theme=light' if query else 'theme=light'
                    record.embed_code = '<iframe src="//www.youtube-nocookie.com/embed/%s?%s" allowFullScreen="true" frameborder="0"></iframe>' % (record.document_id, query)
                else:
                    # embed google doc video
                    record.embed_code = '<iframe src="//drive.google.com/file/d/%s/preview" allowFullScreen="true" frameborder="0"></iframe>' % (record.document_id)
            else:
                record.embed_code = False
