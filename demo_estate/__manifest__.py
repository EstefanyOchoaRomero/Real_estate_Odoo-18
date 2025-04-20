# -*- coding: utf-8 -*-
{
    'name': "demo_estate",

    'summary': "Manage real estate properties",

    'description': """
This module allows you to manage real estate properties.
You can register and view properties for sale or rent.
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Real Estate',
    'version': '0.1',

    # Required modules for this one to work properly
    'depends': ['base'],

    # Always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/estate_property_view.xml',
        'views/estate_property_form.xml',
        'views/estate_property_tree.xml',
        'views/estate_property_action.xml',
        'views/estate_property_menu.xml'
    ],

    # Only loaded in demo mode
    'demo': [
        'demo/demo.xml',
    ],
}

