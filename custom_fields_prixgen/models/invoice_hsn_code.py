from odoo import models, fields, api, _

class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	@api.multi
	def _prepare_invoice_line(self, qty):
		self.ensure_one()
		res = {}
		account = self.product_id.property_account_income_id or self.product_id.categ_id.property_account_income_categ_id
		if not account:
			raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
				(self.product_id.name, self.product_id.id, self.product_id.categ_id.name))
		fpos = self.order_id.fiscal_position_id or self.order_id.partner_id.property_account_position_id
		if fpos:
				account = fpos.map_account(account)
		res = {
			'name': self.name,
			'sequence': self.sequence,
			'origin': self.order_id.name,
			'account_id': account.id,
			'price_unit': self.price_unit,
			'quantity': qty,
			'discount': self.discount,
			'uom_id': self.product_uom.id,
			'product_id': self.product_id.id or False,
			#'layout_category_id': self.layout_category_id and self.layout_category_id.id or False,
			'invoice_line_tax_ids': [(6, 0, self.tax_id.ids)],
			'account_analytic_id': self.order_id.analytic_account_id.id,
			'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
			'l10n_in_hsn': self.l10n_in_hsn,
		}
		return res

	@api.multi
	def _compute_tax_id(self):
		for line in self:
			fpos = line.order_id.fiscal_position_id or line.order_id.partner_id.property_account_position_id
			taxes = line.product_id.taxes_id.filtered(lambda r: not line.company_id or r.company_id == line.company_id)
			line.tax_id = fpos.map_tax(taxes, line.product_id, line.order_id.partner_shipping_id) if fpos else taxes