from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    quantity = fields.Float('Quantity ', default='0', store=True)
    partner_id = fields.Many2one('res.partner', string='Vendor')
    price_unit = fields.Float('Price Unit', default='0')
    quick_uom_po_id = fields.Many2one('uom.uom', string="Quick Unit of Measure")
    # uom_id = fields.Many2one(comodel_name="uom.uom", string="Quick Unit of Measure")
