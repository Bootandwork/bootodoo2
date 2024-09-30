# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Boot&work sale',
    'version': '1.0',
    'author': "Rapsodoo",
    'summary': '',
    'description': """ """,
    'category': 'Uncategorize',
    # 'website': 'https://www.odoo.com/app/invoicing',
    # 'images' : ['images/accounts.jpeg','images/bank_statement.jpeg','images/cash_register.jpeg','images/chart_of_accounts.jpeg','images/customer_invoice.jpeg','images/journal_entries.jpeg'],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'sale',
    ],
    'data': [
        # 'security/ir.model.access.csv',
    ],
    'demo': [],
}
