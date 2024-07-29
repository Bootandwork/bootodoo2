# -*- coding: utf-8 -*-
{
    'name': 'Sale Order Count',
    'version': '16.0.0.0.0',
    'description': "Confirmed Sale Order Count",
    'author': 'IPGrup',
    'company': 'IPGrup',
    'maintainer': 'Gerard - ggonzalez@ipgrup.com',
    'website': 'https://www.ipgrup.com',
    'depends': ['contacts', 'sale'],
    'data': [
        'views/res_partner.xml',
        'views/sale_order.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
