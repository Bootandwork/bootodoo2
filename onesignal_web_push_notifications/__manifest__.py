# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Kinfinity Tech Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'OneSignal Web Push Notifications',
    'version': '11.0.1.0.0',
    'category': 'Website',
    'summary': 'OneSignal Web Push Notifications',
    "author": "Kinfinity Tech Pvt. Ltd.",
    'website': 'http://www.kinfinitytech.com',
    'description': """
OneSignal Web push notifications.
=================================

This module allows to sends personalized web push notifications
to subscribed users from websites.

https://onesignal.com

https://documentation.onesignal.com/docs/web-push-typical-setup
""",
    'depends': ['website'],
    'data': [
        'views/templates.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 25,
    'license': 'OPL-1',
    'currency': 'EUR',
}
