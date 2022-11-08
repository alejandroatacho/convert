
import logging

from odoo import models, fields, api
import datetime

_logger = logging.getLogger(__name__)

class PurchaseOrderveHerit(models.Model):
    _inherit = 'purchase.order'
    lien_vers_al = fields.Many2one('quicklast', string='Lien vers quick list')

    def action_send_mail(self):
        template_id = self.env.ref('purchase.email_template_edi_purchase_done')
        ctx = dict(
            default_model='purchase.order',
            default_res_id=self.id,
            default_email_from=self.env.user.email,
            default_email_to=self.partner_id.email,
            default_use_template=bool(template_id),
            default_template_id=template_id,
            default_composition_mode='comment',
            default_force_email= True,
            default_mark_rfq_as_sent= True,
            custom_layout= 'mail.mail_notification_paynow',
            default_model_description='Purchase Order',
            active_id= self.ids[0],
        )
        mail_mail = self.env['mail.template'].with_context(ctx).browse(template_id.id)
        # # mail_values = {
        # #     'email_from': self.email_from,
        # #     'author_id': self.env.user.id,
        # #     'model': 'purchase.order',
        # #     'res_id': self.id,
        # #     'subject': mail_mail.subject,
        # #     'body_html': mail_mail.body_html,
        # #     # 'attachment_ids': [(4, att.id) for att in self.attachment_ids],
        # #     # 'auto_delete': True,
        # # }
        # mail_mail.email_from = self.env.user.email
        # mail_mail.email_to = self.partner_id.email
        mail_send = mail_mail.send_mail(self.id,force_send=True, email_values={'model': 'purchase.order', 'res_id': self.id,'auto_delete': False})
        # sent = self.env['mail.mail'].browse(mail_send).send()
        mail_mail_sent = self.env['mail.mail'].search([('id','=',mail_send)])
        sent = mail_mail_sent.send()
        print("Mail sent",mail_mail,mail_mail_sent)


class ProductTemplateInherit(models.Model):
    _inherit = 'product.product'

    qte_product = fields.Float('Quantity ', default='0', store=True)
    partner_id = fields.Many2one('res.partner', string='Vendor')
    price_purchase = fields.Float('Purchase price', default='0')
    quick_uom_po_id = fields.Many2one(comodel_name="uom.uom", string="Quick Unit of Measure")

class ProductQuick(models.Model):
    _name = 'productquicktemplate'


    quick_product_id = fields.Many2one('product.product',string='Product')
    quick_qte_product = fields.Float('Quantity ', default='0', store=True)
    uom_po_id = fields.Many2one(comodel_name="uom.uom", string="Unit of Measure")
    quick_vendor_num = fields.Many2one('res.partner', string='Vendor')
    quick_price_purchase = fields.Float('Purchase price', default='0')
    quick_quicklast = fields.Many2one('quicklast', string='QuickID')


    def action_add(self):
        self.quick_quicklast.track = 'closed'
        self.quick_qte_product +=1
        self.with_context(added='added').quick_product_id.qte_product = self.quick_qte_product

    def action_remove(self):
        self.quick_quicklast.track = 'closed'
        if self.quick_qte_product > 0:
            self.quick_qte_product -= 1
            self.quick_product_id.qte_product = self.quick_qte_product
        else:
            self.quick_qte_product = 0
            self.quick_product_id.qte_product = self.quick_qte_product

    @api.onchange('quick_vendor_num','quick_price_purchase')
    def update(self):
        self.quick_product_id.partner_id = self.quick_vendor_num
        self.quick_product_id.price_purchase = self.quick_price_purchase

    @api.onchange('quick_qte_product')
    def update_qte(self):
        self.quick_product_id.qte_product = self.quick_qte_product

    @api.onchange('quick_product_id')
    def onchange_quick_product_id(self):
        if self.quick_product_id:
            self.uom_po_id = self.quick_product_id.uom_po_id.id
        else:
            self.uom_po_id = False

    @api.onchange('uom_po_id')
    def onchange_uom_po_id(self):
        if self.quick_product_id:
            self.quick_product_id.quick_uom_po_id = self.uom_po_id


class QuikListlast(models.Model):
    _name = 'quicklast'
    _description = 'Quik List help'
    _order = 'name asc'

    name = fields.Char('Name', default="Quick Order list")
    qck_ProductQuick_id = fields.One2many('productquicktemplate', string=False, inverse_name='quick_quicklast')
    reset = fields.Char("Reset",compute="compute_reset")
    track = fields.Char("Tarck",default=lambda self: self._context.get('form'))

    def compute_reset(self):
        for rec in self:
            for line in rec.qck_ProductQuick_id:
                if rec.track == 'open':
                    line.quick_qte_product = 0
                    # rec.track = 'closed'
            for line in rec.qck_ProductQuick_id:
                rec.track = 'open'
            rec.reset = 0

    def name_get(self):
        cour_s = []
        for rec in self:
            cour_s.append((rec.id, 'Quick List' ))
        return cour_s

    def send_po(self):
        purchase_id = self.env['purchase.order']
        products_ids = self.env['product.product'].search([])
        product_list = []
        partner_ids = []
        for product in products_ids:
            if product.qte_product > 0:
                product_list.append(product)
                if product.partner_id:
                    partner = product.partner_id
                    if product.partner_id not in partner_ids:
                        partner_ids.append(partner)
        for partner in partner_ids:
            vals = {'partner_id': partner.id,
                    'company_id': self.env.user.company_id.id,
                    'date_planned': datetime.datetime.now(),
                    'lien_vers_al': self.id,
                    'state':'purchase',
                    'date_approve':datetime.datetime.now(),
                    }
            purchase_id = self.env['purchase.order'].sudo().create(vals)
            for product in product_list:
                if product.partner_id == partner:
                    vals = {'product_id': product.id,
                            'name': product.name,
                            'order_id': purchase_id.id,
                            'price_unit': product.price_purchase,
                            'product_qty': product.qte_product,
                            # 'display_type':'line_note',
                            # 'product_uom': product.quick_uom_po_id and product.quick_uom_po_id.id or product.uom_id.id,
                            'product_uom': product.uom_id.id,
                            'date_planned':purchase_id.date_planned or fields.Datetime.now,
                            }
                    # _logger.info('Val of PO ', vals)
                    # _logger.info("val of product.uom_id",product.uom_id)
                    # _logger.info("val of product.quick_uom_po_id",product.quick_uom_po_id)
                    # print("val of po",vals)
                    # print("val of product.uom_id",product.uom_id)
                    # print("val of product.quick_uom_po_id",product.quick_uom_po_id)
                    self.env['purchase.order.line'].create(vals)
                    product.update({'qte_product': 0})
            for line in self.qck_ProductQuick_id:
                line.quick_qte_product = 0
            if purchase_id:
                purchase_id.action_send_mail()

    #lien vers purchase order

    purcahse_order_count = fields.Integer(string="Purchase Count", compute="compute_purchase_count")

    def compute_purchase_count(self):
        for rec in self:
            order_count = self.env['purchase.order'].search_count([('lien_vers_al', '=', rec.id)])
            rec.purcahse_order_count = order_count

    def action_open_rfq(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchases',
            'res_model': 'purchase.order',
            'view_type': 'form',
            'domain': [('lien_vers_al', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',

        }




