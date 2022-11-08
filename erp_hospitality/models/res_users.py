# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class Users(models.Model):
    _inherit = "res.users"

    is_account_user = fields.Boolean(default=False)

    def write(self, vals):
        res = super(Users, self).write(vals)
        # if self.env.ref('erp_hospitality.group_erp_hospitality').id in self.groups_id.ids:
        #     discuss_menu_id = self.env.ref('mail.menu_root_discuss')
        #     discuss_menu_id.sudo().write({
        #         'groups_id' : [(3, self.env.ref('base.group_user').id)]
        #     })
        #     website_menu_id = self.env.ref('website.menu_website_configuration')
        #     website_menu_id.sudo().write({
        #         'groups_id' : [(3, self.env.ref('base.group_user').id)]
        #     })
        #     calendar_menu_id = self.env.ref('calendar.mail_menu_calendar')
        #     calendar_menu_id.sudo().write({
        #         'groups_id' : [(3, self.env.ref('base.group_user').id)]
        #     })
        if self.env.ref('erp_hospitality.group_erp_hospitality').id not in self.groups_id.ids:
            # discuss_menu_id = self.env.ref('mail.menu_root_discuss')
            # discuss_menu_id.sudo().write({
            #     'groups_id' : [(4, self.env.ref('base.group_user').id)]
            # })
            # website_menu_id = self.env.ref('website.menu_website_configuration')
            # website_menu_id.sudo().write({
            #     'groups_id' : [(4, self.env.ref('base.group_user').id)]
            # })
            # calendar_menu_id = self.env.ref('calendar.mail_menu_calendar')
            # calendar_menu_id.sudo().write({
            #     'groups_id' : [(4, self.env.ref('base.group_user').id)]
            # })
            back_office_menu_id = self.env.ref('erp_hospitality.menu_back_office')
            back_office_menu_id.sudo().write({
                'groups_id' : [(4, self.env.ref('erp_hospitality.group_erp_hospitality').id)]
            })

        if self.env.ref('erp_hospitality.group_erp_hospitality').id in self.groups_id.ids and \
            self.env.ref('account.group_account_invoice').id in self.groups_id.ids:
            group_id = self.env.ref('erp_hospitality.group_erp_back_to_office')
            group_id.sudo().write({
                'users' : [(4, self.id)] 
            })
        
        if self.env.ref('account.group_account_invoice').id not in self.groups_id.ids:
            group_id = self.env.ref('erp_hospitality.group_erp_back_to_office')
            group_id.sudo().write({
                'users' : [(3, self.id)] 
            })

        # if self.env.ref('erp_hospitality.group_erp_back_to_office').id in self.groups_id.ids and \
        #     self.env.ref('account.group_account_invoice').id in self.groups_id.ids:

        #     account_menu_id = self.env.ref('account_accountant.menu_accounting')
        #     account_menu_id.sudo().write({
        #         'groups_id' : [(6, 0, [self.env.ref('erp_hospitality.group_erp_back_to_hospitality').id])]
        #     })

        if self.env.ref('erp_hospitality.group_erp_hospitality').id not in self.groups_id.ids:
            account_menu_id = self.env.ref('account_accountant.menu_accounting')
            account_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    self.env.ref('account.group_account_invoice').id,
                    self.env.ref('account.group_account_readonly').id,])]
            })

        return res