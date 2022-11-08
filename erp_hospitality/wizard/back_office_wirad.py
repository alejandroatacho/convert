# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class BackOfficeWizard(models.TransientModel):
    _name = 'back.office'
    _description = 'Back Office'


    def back_to_office_action(self):
        user_id = self.env.user

        if user_id.has_group('erp_hospitality.group_erp_hospitality_account_receive'):
            # pos_menu_id = self.env.ref('erp_hospitality.menu_erp_hospitality')
            # pos_menu_id.sudo().write({
            #     'groups_id' : [(3, self.env.ref('erp_hospitality.group_erp_hospitality_account_receive').id)]
            # })
            # print(stop)
            # receive_menu_id = self.env.ref('erp_hospitality.menu_account_receive')
            # receive_menu_id.sudo().write({
            #     'groups_id' : [(3, self.env.ref('erp_hospitality.group_erp_hospitality_account_receive').id)]
            # })

            user_id.sudo().write({
                'groups_id' : [(3, self.env.ref('erp_hospitality.group_erp_hospitality_account_receive').id)],
                'is_account_user' : True
            })

            # print(":::::receive_menu_id",receive_menu_id.groups_id)

            # quick_order_list_menu_id = self.env.ref('erp_hospitality.menu_erp_hospitality_quick_order_list')
            # quick_order_list_menu_id.sudo().write({
            #     'groups_id' : [(6,0,[self.env.ref('website_calendar_booking.group_reservation_management_user').id])]
            # })

            # reservation_menu_id = self.env.ref('erp_hospitality.main_menu_erp_hospitality_reservation_management')
            # reservation_menu_id.sudo().write({
            #     'groups_id' : [(3, self.env.ref('erp_hospitality.group_erp_hospitality_account_receive').id)]
            # })
            
            back_office_menu_id = self.env.ref('erp_hospitality.menu_back_office')
            back_office_menu_id.sudo().write({
                'groups_id' : [(3,self.env.ref('erp_hospitality.group_erp_hospitality_account_receive').id)]
            })

        user_id.sudo().write({
            'groups_id' : [(3, self.env.ref('erp_hospitality.group_erp_hospitality').id)]
        })

        group_id = self.env.ref('erp_hospitality.group_erp_back_to_hospitality')
        group_id.sudo().write({
            'users' : [(4, user_id.id)] 
        })

        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/web',
            
        }