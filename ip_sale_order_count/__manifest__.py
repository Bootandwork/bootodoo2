# -*- coding: utf-8 -*-
{
    'name': 'Sale Order Count',
    'version': '16.0.0.0.0',
    'description': "Custom module for MontexFR",
    'author': 'IPGrup',
    'company': 'IPGrup',
    'maintainer': 'Gerard - ggonzalez@ipgrup.com',
    'website': 'https://www.ipgrup.com',
    'depends': ['contacts', 'sale'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
