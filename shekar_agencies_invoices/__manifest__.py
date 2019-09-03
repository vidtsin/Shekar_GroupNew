{
    'name': 'Shekar agencies invoice Model',
    'version': '12.1.1.1',
    'category': 'Tools',
    'summary': "This module consists, the customized Templates",
    'depends': ['account_tax_python','account','l10n_in','custom_fields_shekar'],
    'website': 'http://www.prixgen.com',
    'data': [
             'views/report_invoice_document_inherit.xml',
             'views/tax_amount.xml',
             ],
    'auto_install': False,
    'application': True,
}
