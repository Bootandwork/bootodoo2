# Copyright © 2023 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

{
    'name': 'Website | eCommerce Tracking Base',
    'version': '16.0.1.2.0',
    'category': 'eCommerce',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz/en/odoo-website-tracking',
    'license': 'OPL-1',
    'summary': 'Track Customer Actions on Odoo Website and eCommerce',
    'depends': [
        'website_sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/website_views.xml',
        'views/website_sale_templates.xml',
        'views/website_tracking_service_views.xml',
        'views/website_tracking_log_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_sale_tracking_base/static/src/js/website_sale_tracking.js',
            'website_sale_tracking_base/static/src/js/website_login_tracking.js',
            'website_sale_tracking_base/static/src/js/checkout_form_tracking.js',
            'website_sale_tracking_base/static/src/js/website_tracking.js',
        ],
    },
    'price': 10.0,
    'currency': 'EUR',
    'support': 'support@garazd.biz',
    'application': True,
    'installable': True,
    'auto_install': False,
}
