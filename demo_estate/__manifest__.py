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
    'version': '18.0.1.0.6',

    # Required modules for this one to work properly
    'depends': ['base', 'account'],

    # Always loaded
    'data': [

        'security/ir.model.access.csv',

        # Firts views
        'views/estate_property_views.xml',
        'views/estate_menus.xml',

        # Later reports
        'report/estate_property_templates.xml',
        'report/estate_property_offers_report.xml',

        # Finally, the actions that use those templates
        'report/estate_property_report.xml',

    ],

}
