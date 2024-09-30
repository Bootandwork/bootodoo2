# Copyright © 2021 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

# flake8: noqa: E501

{
    'name': 'Google Analytics 4 Global Site Tag (gtag.js)',
    'version': '16.0.2.0.0',
    'category': 'Website',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz/shop',
    'license': 'OPL-1',
    'summary': 'Google Analytics 4 Global Site Tag (gtag.js) | Odoo GA4 integration',
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'live_test_url': 'https://garazd.biz/r/CN9',
    'depends': [
        'website',
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/website_templates.xml',
    ],
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
