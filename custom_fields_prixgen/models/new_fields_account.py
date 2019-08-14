# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from odoo import api, fields, models, _
class AccountInvoice(models.Model):
	_inherit = 'account.invoice'
	payment_method = fields.Char(string='Payment method',store=True)
	ext_doc_no = fields.Char(string='External Document No', store=True)
	custom_po_no = fields.Char(string='PO NO', store=True)
	po_date = fields.Char(string='PO Date', store=True)
	vehicle = fields.Many2one('fleet.vehicle',string='vehicle')
	l10n_in_hsn = fields.Char('HSN Code', store=True)
	confirmation_date = fields.Date(string='Confirmation Date')
