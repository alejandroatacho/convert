# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import AccessError


class BackPOSWizard(models.TransientModel):
    _name = 'back.pos'
    _description = 'Back POS'


    def action_back_to_pos(self):
        user_id = self.env.user

        if self.env.user.has_group('erp_hospitality.group_erp_hospitality_account_receive'):
            raise AccessError(_("You don't have the access rights for POS."))
        elif self.env.user.has_group('erp_hospitality.group_erp_hospitality_quick_order_reservation_receive'):
            raise AccessError(_("You don't have the access rights for POS."))
        elif self.env.user.has_group('erp_hospitality.group_erp_hospitality_quick_order_receive'):
            raise AccessError(_("You don't have the access rights for POS."))