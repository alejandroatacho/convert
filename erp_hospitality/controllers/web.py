# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.addons.web.controllers import main
from odoo.http import request


class Home(main.Home):


    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):

        if request.env['res.users'].sudo().browse(request.session.uid).has_group('erp_hospitality.group_erp_back_to_office') and \
            request.env['res.users'].sudo().browse(request.session.uid).has_group('account.group_account_manager'):

            account_menu_id = request.env.ref('account_accountant.menu_accounting')
            account_menu_id.sudo().write({
                'groups_id' : [(6, 0, [request.env.ref('erp_hospitality.group_erp_back_to_hospitality').id])]
            })

        if not request.env['res.users'].sudo().browse(request.session.uid).has_group('erp_hospitality.group_erp_hospitality'):
            account_menu_id = request.env.ref('account_accountant.menu_accounting')
            account_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('account.group_account_invoice').id,
                    request.env.ref('account.group_account_readonly').id,])]
            })

            discuss_menu_id = request.env.ref('mail.menu_root_discuss')
            discuss_menu_id.sudo().write({
                'groups_id' : [(6,0,[request.env.ref('base.group_user').id])]
            })

            calendar_menu_id = request.env.ref('calendar.mail_menu_calendar')
            calendar_menu_id.sudo().write({
                'groups_id' : [(6,0,[request.env.ref('base.group_user').id])]
            })

            website_menu_id = request.env.ref('website.menu_website_configuration')
            website_menu_id.sudo().write({
                'groups_id' : [(6,0,[request.env.ref('base.group_user').id])]
            })

            contact_menu_id = request.env.ref('contacts.menu_contacts')
            contact_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('base.group_partner_manager').id,
                    request.env.ref('base.group_user').id])]
            })

        if request.env['res.users'].sudo().browse(request.session.uid).has_group('erp_hospitality.group_erp_hospitality') or \
            request.env['res.users'].sudo().browse(request.session.uid).has_group('erp_hospitality.group_erp_back_to_office') or \
            request.env['res.users'].sudo().browse(request.session.uid).has_group('erp_hospitality.group_erp_back_to_hospitality'):
            
            discuss_menu_id = request.env.ref('mail.menu_root_discuss')
            discuss_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('sales_team.group_sale_salesman').id,
                    request.env.ref('sales_team.group_sale_salesman_all_leads').id,
                    request.env.ref('stock.group_stock_user').id,
                    request.env.ref('purchase.group_purchase_user').id,])]
            })

            calendar_menu_id = request.env.ref('calendar.mail_menu_calendar')
            calendar_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('sales_team.group_sale_salesman').id,
                    request.env.ref('sales_team.group_sale_salesman_all_leads').id,
                    request.env.ref('stock.group_stock_user').id,
                    request.env.ref('purchase.group_purchase_user').id,])]
            })

            website_menu_id = request.env.ref('website.menu_website_configuration')
            website_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('website.group_website_designer').id,
                    request.env.ref('website.group_website_publisher').id])]
            })

            contact_menu_id = request.env.ref('contacts.menu_contacts')
            contact_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('base.group_partner_manager').id])]
            })


        if request.env['res.users'].sudo().browse(request.session.uid).has_group('erp_hospitality.group_erp_hospitality') and \
            not request.env['res.users'].sudo().browse(request.session.uid).has_group('erp_hospitality.group_erp_back_to_office'):
            # print(stop)
            back_office_menu_id = request.env.ref('erp_hospitality.menu_back_office')
            back_office_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('erp_hospitality.group_erp_back_to_office').id])]
            })

        if request.env['res.users'].sudo().browse(request.session.uid).has_group('erp_hospitality.group_erp_hospitality_account_receive'):
            # account_menu_id = request.env.ref('account_accountant.menu_accounting')
            # account_menu_id.sudo().write({
            #     'groups_id' : [(6, 0, [request.env.ref('erp_hospitality.group_erp_hospitality_account_receive').id])]
            # })

            # back_office_menu_id = request.env.ref('erp_hospitality.menu_back_office')
            # back_office_menu_id.sudo().write({
            #     'groups_id' : [(6,0,[
            #         request.env.ref('erp_hospitality.group_erp_hospitality_account_receive').id])]
            # })

            account_menu_id = request.env.ref('account_accountant.menu_accounting')
            account_menu_id.sudo().write({
                'groups_id' : [(6, 0, [request.env.ref('erp_hospitality.group_erp_back_to_hospitality').id])]
            })

            back_office_menu_id = request.env.ref('erp_hospitality.menu_back_office')
            back_office_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('erp_hospitality.group_erp_hospitality_account_receive').id])]
            })

            discuss_menu_id = request.env.ref('mail.menu_root_discuss')
            discuss_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('sales_team.group_sale_salesman').id,
                    request.env.ref('sales_team.group_sale_salesman_all_leads').id,
                    request.env.ref('stock.group_stock_user').id,
                    request.env.ref('purchase.group_purchase_user').id,])]
            })

            calendar_menu_id = request.env.ref('calendar.mail_menu_calendar')
            calendar_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('sales_team.group_sale_salesman').id,
                    request.env.ref('sales_team.group_sale_salesman_all_leads').id,
                    request.env.ref('stock.group_stock_user').id,
                    request.env.ref('purchase.group_purchase_user').id,])]
            })

            website_menu_id = request.env.ref('website.menu_website_configuration')
            website_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('website.group_website_designer').id,
                    request.env.ref('website.group_website_publisher').id])]
            })

            contact_menu_id = request.env.ref('contacts.menu_contacts')
            contact_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('base.group_partner_manager').id])]
            })

        if request.env['res.users'].sudo().browse(request.session.uid).has_group('erp_hospitality.group_erp_hospitality_quick_order_reservation_receive'):
            discuss_menu_id = request.env.ref('mail.menu_root_discuss')
            discuss_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('sales_team.group_sale_salesman').id,
                    request.env.ref('sales_team.group_sale_salesman_all_leads').id,
                    request.env.ref('stock.group_stock_user').id,
                    request.env.ref('purchase.group_purchase_user').id,])]
            })

            calendar_menu_id = request.env.ref('calendar.mail_menu_calendar')
            calendar_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('sales_team.group_sale_salesman').id,
                    request.env.ref('sales_team.group_sale_salesman_all_leads').id,
                    request.env.ref('stock.group_stock_user').id,
                    request.env.ref('purchase.group_purchase_user').id,])]
            })

            website_menu_id = request.env.ref('website.menu_website_configuration')
            website_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('website.group_website_designer').id,
                    request.env.ref('website.group_website_publisher').id])]
            })

            contact_menu_id = request.env.ref('contacts.menu_contacts')
            contact_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('base.group_partner_manager').id])]
            })

        if request.env['res.users'].sudo().browse(request.session.uid).has_group('erp_hospitality.group_erp_hospitality_quick_order_receive'):
            discuss_menu_id = request.env.ref('mail.menu_root_discuss')
            discuss_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('sales_team.group_sale_salesman').id,
                    request.env.ref('sales_team.group_sale_salesman_all_leads').id,
                    request.env.ref('stock.group_stock_user').id,
                    request.env.ref('purchase.group_purchase_user').id,])]
            })

            calendar_menu_id = request.env.ref('calendar.mail_menu_calendar')
            calendar_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('sales_team.group_sale_salesman').id,
                    request.env.ref('sales_team.group_sale_salesman_all_leads').id,
                    request.env.ref('stock.group_stock_user').id,
                    request.env.ref('purchase.group_purchase_user').id,])]
            })

            website_menu_id = request.env.ref('website.menu_website_configuration')
            website_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('website.group_website_designer').id,
                    request.env.ref('website.group_website_publisher').id])]
            })

            contact_menu_id = request.env.ref('contacts.menu_contacts')
            contact_menu_id.sudo().write({
                'groups_id' : [(6,0,[
                    request.env.ref('base.group_partner_manager').id])]
            }) 

        return super(Home, self).web_client(s_action, **kw)