# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import AccessError


class BackReservationWizard(models.TransientModel):
    _name = 'back.reservation'
    _description = 'Back Reservation'


    def action_back_to_reservation(self):
        user_id = self.env.user

        if self.env.user.has_group('erp_hospitality.group_erp_hospitality_account_receive'):
            raise AccessError(_("You don't have the access rights for Reservation."))
        elif self.env.user.has_group('erp_hospitality.group_erp_hospitality_quick_order_receive'):
            raise AccessError(_("You don't have the access rights for Reservation."))