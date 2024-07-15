# invoice_last_payment_date/__manifest__.py
{
    'name': 'Invoice Last Payment Date',
    'version': '1.0',
    'summary': 'Adds a field to store the date of the last payment on invoices',
    'author': 'IPGrup',
    'category': 'Accounting',
    'depends': ['account'],
    'data': [
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
}
