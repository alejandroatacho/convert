# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class BackDashboardWizard(models.TransientModel):
    _name = 'back.dashboard'
    _description = 'Back Dashboard'


    def back_to_dashboard_action(self):
        user_id = self.env.user

        if user_id.has_group('erp_hospitality.group_erp_hospitality_account_receive') or user_id.is_account_user:
            # pos_menu_id = self.env.ref('erp_hospitality.menu_erp_hospitality')
            # pos_menu_id.sudo().write({
            #     'groups_id' : [(4, self.env.ref('erp_hospitality.group_erp_hospitality_account_receive').id)]
            # })

            # quick_order_list_menu_id = self.env.ref('erp_hospitality.menu_erp_hospitality_quick_order_list')
            # quick_order_list_menu_id.sudo().write({
            #     'groups_id' : [(4, self.env.ref('erp_hospitality.group_erp_hospitality_account_receive').id)]
            # })

            # reservation_menu_id = self.env.ref('erp_hospitality.main_menu_erp_hospitality_reservation_management')
            # reservation_menu_id.sudo().write({
            #     'groups_id' : [(4, self.env.ref('erp_hospitality.group_erp_hospitality_account_receive').id)]
            # })

            back_office_menu_id = self.env.ref('erp_hospitality.menu_back_office')
            back_office_menu_id.sudo().write({
                'groups_id' : [(4,self.env.ref('erp_hospitality.group_erp_hospitality_account_receive').id)]
            })

            receive_menu_id = self.env.ref('erp_hospitality.menu_account_receive')
            receive_menu_id.sudo().write({
                'groups_id' : [(4, self.env.ref('erp_hospitality.group_erp_hospitality_account_receive').id)]
            })

            user_id.sudo().write({
                'groups_id' : [(4, self.env.ref('erp_hospitality.group_erp_hospitality_account_receive').id)],
                'is_account_user' : False
            })

            user_id.sudo().write({
                'groups_id' : [(3, self.env.ref('erp_hospitality.group_erp_back_to_hospitality').id)]
            })
        else:

            user_id.sudo().write({
                'groups_id' : [(3, self.env.ref('erp_hospitality.group_erp_back_to_hospitality').id)]
            })

            user_id.sudo().write({
                'groups_id' : [(4, self.env.ref('erp_hospitality.group_erp_hospitality').id)]
            })
        
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/web',
        }