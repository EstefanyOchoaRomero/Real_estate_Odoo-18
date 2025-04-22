# -*- coding: utf-8 -*-
{
    'name': "demo_estate",

    'summary': "Manage real estate properties",

    'description': """
This module allows you to manage real estate properties.
You can register and view properties for sale or rent.
    """,

    'author': "TiOdoo.S.L.",
    'website': "https://www.yourcompany.com",

    'category': 'Real Estate',
    'version': '18.0.1.0.1',

    # Required modules for this one to work properly
    'depends': ['base'],

    # Always loaded
    'data': [
        'security/ir.model.access.csv',
        
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        
    ],

    # Only loaded in demo mode
    'demo': [
        'demo/demo.xml',
    ],
}
        

