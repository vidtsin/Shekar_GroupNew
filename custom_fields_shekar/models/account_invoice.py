from odoo import api, fields, models, _

class AccountInvoice(models.Model):
	_inherit = 'account.invoice'

	payment_method = fields.Char(string='Payment method',store=True)
	ext_doc_no = fields.Char(string='External Document No', store=True)
	custom_po_no = fields.Char(string='PO NO', store=True)
	po_date = fields.Char(string='PO Date', store=True)
	vehicle = fields.Many2one('fleet.vehicle',string='vehicle')
	confirmation_date = fields.Datetime(string='Confirmation Date')
	order_type = fields.Char(string='Order Type',store=True)
	pricelist_id = fields.Many2one('product.pricelist',string="Pricelist")


class AccountInvoiceLine(models.Model):
	_inherit = 'account.invoice.line'


	l10n_in_hsn = fields.Char('HSN Code',compute = "_onchange_product_id_hsn")


	@api.depends('product_id')
	def _onchange_product_id_hsn(self):
		for line in self:
			line.l10n_in_hsn = "%s" % (line.product_id.l10n_in_hsn_code or "")