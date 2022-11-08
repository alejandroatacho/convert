from odoo import api, models, fields, _


class Partner(models.Model):

	_inherit = 'res.partner'


	def action_view_bill_waiting_receive_po(self):
		partner_id = self.with_context(active_test=False).search([('id', '=', self.id)])
		action = self.with_context(active_id=self.id, active_ids=self.ids) \
			.env.ref('erp_hospitality.act_show_all_receive_po') \
			.sudo().read()[0]
		action['display_name'] = self.name
		action['domain'] = [('invoice_status','=', 'to invoice'),('partner_id', '=', partner_id.id)] 
		return action

	
	def action_view_receive_po(self):
		all_partners = self.with_context(active_test=False).search([('id', 'child_of', self.ids)])
		all_partners.read(['parent_id'])
		action = self.with_context(active_id=self.id, active_ids=self.ids) \
			.env.ref('erp_hospitality.act_show_all_receive_po') \
			.sudo().read()[0]
		action['display_name'] = self.name
		action['domain'] = [('picking_ids.state', 'not in', ('done', 'cancel')),('partner_id', 'in', all_partners.ids)] 
		return action


	def _compute_purchase_order_count(self):

        # retrieve all children partners and prefetch 'parent_id' on them
		all_partners = self.with_context(active_test=False).search([('id', 'child_of', self.ids)])
		all_partners.read(['parent_id'])

		purchase_order_groups = self.env['purchase.order'].read_group(
			domain=[('partner_id', 'in', all_partners.ids)],
			fields=['partner_id'], groupby=['partner_id']
		)
		
		if self.env.context.get('search_default_receive_po'):
			purchase_order_groups = self.env['purchase.order'].read_group(
				domain=[('partner_id', 'in', all_partners.ids),
				('picking_ids.state', 'not in', ('done', 'cancel'))],
				fields=['partner_id'], groupby=['partner_id']
			)

		partners = self.browse()
		for group in purchase_order_groups:
			partner = self.browse(group['partner_id'][0])
			while partner:
				if partner in self:
					partner.partner_picking_order_count = 0
					partner.partner_picking_order_count += group['partner_id_count']
					partner.purchase_order_count += group['partner_id_count']
					partners |= partner
				partner = partner.parent_id
		(self - partners).partner_picking_order_count = 0
		(self - partners).purchase_order_count = 0
		# print(stop)


	def compute_bill_waiting_status(self):
		for record in self:
			record.account_bill_waiting_count = 0
			po_ids = record.mapped('purchase_line_ids.order_id')
			for po_id in po_ids:
				if po_id.invoice_status == 'to invoice':
					record.account_bill_waiting_count += 1

	partner_picking_order_count = fields.Integer()
	receive_picking_ids = fields.Many2many('stock.picking')
	account_bill_waiting_count = fields.Integer(compute="compute_bill_waiting_status")


