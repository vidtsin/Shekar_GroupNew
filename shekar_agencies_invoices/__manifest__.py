{
    'name': 'Shekart agencies invoice Model',
    'version': '12.0.1',
    'category': 'Tools',
    'summary': "This module consists, the customized Templates",
    'depends': ['account_tax_python','account','l10n_in','custom_fields_prixgen'],
    'website': 'https://www.prixgen.com',
    'data': [
             'views/report_invoice_document_inherit.xml',
             'views/tax_amount.xml',
             ],
    'auto_install': False,
    'application': True,
}
