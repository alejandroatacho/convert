# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import AccessError


class BackQuickOrderWizard(models.TransientModel):
    _name = 'back.quick.order'
    _description = 'Back Quick Order'


    def action_back_to_quick_order(self):
        user_id = self.env.user

        if self.env.user.has_group('erp_hospitality.group_erp_hospitality_account_receive'):
            raise AccessError(_("You don't have the access rights for Quick Order List."))

    