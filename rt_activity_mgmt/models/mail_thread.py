# -*- coding: utf-8 -*-

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    # ---------------------------------------------------------
    # Messaging
    # ---------------------------------------------------------
    def message_post_with_view(self, views_or_xmlid, **kwargs):
        """ 
            Inherited Method
            Add subject in mail.message when activity is done
        """

        values = kwargs.get('values', None) or dict()
        if values and values.get('activity', False) and kwargs.get('subject', False) == False:
            activity = values.get('activity')
            if len(activity) == 1 and activity.summary:
                kwargs.update({
                    'subject': activity.summary
                })
        return self._message_compose_with_view(views_or_xmlid, **kwargs)
