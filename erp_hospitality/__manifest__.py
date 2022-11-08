# -*- coding: utf-8 -*-
{
    'name': 'ERP Hospitality',
    'summary': "Hospitality Management",
    'version': '14.0.25.0.0',
    'category': 'Tools',
    'author': 'SMART-obc.com',
    'website': 'https://smart-obc.com/',
    'license': 'AGPL-3',
    'depends': ['web','account_accountant','contacts','pos_restaurant','restaurant_purchase_quick_list','website_calendar_booking','purchase_stock'],
    'data': [
        'security/hospitality_security.xml',
        'security/ir.model.access.csv',
        'views/erp_hospitality_view.xml',
        'wizard/back_to_office_wizard_view.xml',
        'wizard/back_to_hosp_wizard_view.xml',
        # 'wizard/back_to_pos_wizard_view.xml',
        # 'wizard/back_to_quick_order_wizard_view.xml',
        # 'wizard/back_to_reservation_wizard_view.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
