import logging

from odoo import models, fields, api
import datetime

_logger = logging.getLogger(__name__)


class QuikListLast(models.Model):
    _name = 'quick.list.last'
    _description = 'Quik List Last'
    _order = 'name asc'

    name = fields.Char('Name', default="Quick Order list")
    product_quick_template_id = fields.One2many('product.quick.template', string=False, inverse_name='quick_list_last')
    reset = fields.Char("Reset", compute="compute_reset")
    track = fields.Char("Tarck", default=lambda self: self._context.get('form'))

    def compute_reset(self):
        for rec in self:
            for line in rec.product_quick_template_id:
                if rec.track == 'open':
                    line.quantity = 0
                    # rec.track = 'closed'
            for line in rec.product_quick_template_id:
                rec.track = 'open'
            rec.reset = 0

    # def name_get(self):
    #     cour_s = []
    #     for rec in self:
    #         cour_s.append((rec.id, 'Quick List'))
    #     return cour_s

    def send_po(self):
        purchase_id = self.env['purchase.order']
        products_ids = self.env['product.product'].search([])
        product_list = []
        partner_ids = []
        for product in products_ids:
            if product.quantity > 0:
                product_list.append(product)
                if product.partner_id:
                    partner = product.partner_id
                    if product.partner_id not in partner_ids:
                        partner_ids.append(partner)
        for partner in partner_ids:
            vals = {'partner_id': partner.id,
                    'company_id': self.env.user.company_id.id,
                    'date_planned': datetime.datetime.now(),
                    'quick_list_last_id': self.id,
                    'state': 'purchase',
                    'date_approve': datetime.datetime.now(),
                    }
            purchase_id = self.env['purchase.order']
            for pqm in self.product_quick_template_id:
                if pqm.partner_id == partner:
                    if pqm.quantity > 0:
                        if not purchase_id:
                            purchase_id = purchase_id.sudo().create(vals)
                        vals = {'product_id': pqm.product_id.id,
                            'name': pqm.product_id.name,
                            'order_id': purchase_id.id,
                            'price_unit': pqm.price_unit,
                            'product_qty': pqm.quantity,
                            # 'display_type':'line_note',
                            # 'product_uom': product.uom_id and product.uom_id.id or product.uom_id.id,
                            'product_uom': pqm.uom_id.id,
                            'date_planned': purchase_id.date_planned or fields.Datetime.now,
                            }
                        # _logger.info('Val of PO ', vals)
                        # _logger.info("val of product.uom_id",product.uom_id)
                        # _logger.info("val of product.uom_id",product.uom_id)
                        self.env['purchase.order.line'].create(vals)
                    # pqm.update({'quantity': 0})
            if purchase_id:
                purchase_id.action_send_mail()

        for line in self.product_quick_template_id:
            line.quantity = 0

    # lien vers purchase order

    purchase_order_count = fields.Integer(string="Purchase Count", compute="compute_purchase_count")

    def compute_purchase_count(self):
        for rec in self:
            order_count = self.env['purchase.order'].search_count([('quick_list_last_id', '=', rec.id)])
            rec.purchase_order_count = order_count

    def action_open_rfq(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchases',
            'res_model': 'purchase.order',
            'view_type': 'form',
            'domain': [('quick_list_last_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }


class ProductQuickTemplate(models.Model):
    _name = 'product.quick.template'

    product_id = fields.Many2one('product.product', string='Product')
    product_uom_id = fields.Many2one(related='product_id.uom_id')
    uom_category_id = fields.Many2one(related='product_uom_id.category_id', store=True)
    quantity = fields.Float('Quantity ', default='0', store=True)
    uom_id = fields.Many2one("uom.uom", string="Unit of Measure", domain="[('category_id','=', uom_category_id)]")
    partner_id = fields.Many2one('res.partner', string='Vendor')
    price_unit = fields.Float('Price Unit', default='0')
    quick_list_last = fields.Many2one('quick.list.last', string='QuickID')

    @api.onchange('quantity')
    def onchange_qty(self):
        self._origin.quick_list_last.track = 'closed'
        pass

    def action_add(self):
        self.quick_list_last.track = 'closed'
        self.quantity += 1
        self.with_context(added='added').product_id.quantity = self.quantity

    def action_remove(self):
        self.quick_list_last.track = 'closed'
        if self.quantity > 0:
            self.quantity -= 1
            self.product_id.quantity = self.quantity
        else:
            self.quantity = 0
            self.product_id.quantity = self.quantity

    @api.onchange('partner_id', 'price_unit')
    def update(self):
        self.product_id.partner_id = self.partner_id
        self.product_id.price_unit = self.price_unit

    @api.onchange('quantity')
    def update_qte(self):
        self.product_id.quantity = self.quantity

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id
        else:
            self.uom_id = False

    # @api.onchange('uom_id')
    # def onchange_uom_id(self):
    #     if self.product_id:
    #         self.product_id.uom_id = self.uom_id
