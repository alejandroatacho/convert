# -*- coding: utf-8 -*-
{
    'name': "QuikListUpdate2",

    'summary': """""",

    'description': """
        
    """,

    'author': "",
    'website': "",

    'category': 'Uncategorized',
    'version': '0.20',

    # any module necessary for this one to work correctly
    'depends': ['purchase', 'sale', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/quick_list_up.xml',
    ],
}
