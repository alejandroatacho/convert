from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    lien_vers_al = fields.Many2one('quicklast', string='Please Dont delete from here causing issue in live bcz it was first created in older version')
    quick_list_last_id = fields.Many2one('quick.list.last', string='Lien vers quick list')

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
            default_force_email=True,
            default_mark_rfq_as_sent=True,
            custom_layout='mail.mail_notification_paynow',
            default_model_description='Purchase Order',
            active_id=self.ids[0],
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
        mail_send = mail_mail.send_mail(self.id, force_send=True,
                                        email_values={'model': 'purchase.order', 'res_id': self.id,
                                                      'auto_delete': False})
        # sent = self.env['mail.mail'].browse(mail_send).send()
        mail_mail_sent = self.env['mail.mail'].search([('id', '=', mail_send)])
        sent = mail_mail_sent.send()
        print("Mail sent", mail_mail, mail_mail_sent)
