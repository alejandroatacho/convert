from odoo import api, models, fields, _


class PurchaseOrder(models.Model):

	_inherit = 'purchase.order'

	def button_confirm(self):
		res = super(PurchaseOrder, self).button_confirm()
		self.partner_id._compute_purchase_order_count()
		return res


	@api.model
	def create(self, vals):
		res = super(PurchaseOrder, self).create(vals)
		if res.quick_list_last_id:
			res.partner_id._compute_purchase_order_count()
		return res