# -*- coding: utf-8 -*-
#############################################################################
#############################################################################

{
    'name': 'JS on Website',
    'version': '16.0.1.0.0',
    'category': 'Tools',
    'depends': ['website'],
    'data': [],
    'images': [],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
    'assets': {
        'web.assets_frontend': [
            'website_js/static/src/js/user_custom_javascript.js'
        ]
    }
}