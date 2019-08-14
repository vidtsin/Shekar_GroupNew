from odoo import models, fields, api, _

class SaleOrder(models.Model):
	_inherit='sale.order'
	advance_amount = fields.Char(string="Advance Amount",store=True)
	payment_method = fields.Many2one('custom.fields',string='Payment method',store=True ,index=True,ondelete='cascade')
	custom_po_no = fields.Char(string='Custom PO Num', store=True)
	ext_doc_no = fields.Char(string='External Document No', store=True)
	po_date = fields.Date(String='PO Date', store=True)
	order_type = fields.Many2one('sale.order.type',string='Order Type',store=True)
	
	@api.multi

	def _prepare_invoice(self):
		self.ensure_one()
		journal_id = self.env['account.invoice'].default_get(['journal_id'])['journal_id']
		if not journal_id:
			raise UserError(_('Please define an accounting sales journal for this company.'))
		invoice_vals = {
			'name': self.client_order_ref or '',
			'origin': self.name,
			'type': 'out_invoice',
			'account_id': self.partner_invoice_id.property_account_receivable_id.id,
			'partner_id': self.partner_invoice_id.id,
			'partner_shipping_id': self.partner_shipping_id.id,
			'journal_id': journal_id,
			'currency_id': self.pricelist_id.currency_id.id,
			'comment': self.note,
			'payment_term_id': self.payment_term_id.id,
			'confirmation_date': self.confirmation_date,
			'payment_method': self.payment_method.name,
			'order_type': self.order_type.name,
			'fiscal_position_id': self.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
			'company_id': self.company_id.id,
			'user_id': self.user_id and self.user_id.id,
			'team_id': self.team_id.id,
			'ext_doc_no': self.ext_doc_no,
			'custom_po_no': self.custom_po_no,
			'po_date': self.po_date,
			'pricelist_id':self.pricelist_id.id,
		}
		return invoice_vals

class SaleOrderType(models.Model):
	_name = "sale.order.type"
	name= fields.Char(store=True ,ondelete='cascade')
	description= fields.Text(string='Description',store=True ,ondelete='cascade')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    l10n_in_hsn = fields.Char('HSN Code',compute = "_onchange_product_id_hsn")

    @api.depends('product_id')
    def _onchange_product_id_hsn(self):
    	for line in self:
    		line.l10n_in_hsn = "%s" % (line.product_id.l10n_in_hsn_code or "")

