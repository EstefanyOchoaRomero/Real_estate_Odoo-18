# -*- coding: utf-8 -*-
# from odoo import http


# class DemoSale(http.Controller):
#     @http.route('/demo_sale/demo_sale', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/demo_sale/demo_sale/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('demo_sale.listing', {
#             'root': '/demo_sale/demo_sale',
#             'objects': http.request.env['demo_sale.demo_sale'].search([]),
#         })

#     @http.route('/demo_sale/demo_sale/objects/<model("demo_sale.demo_sale"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('demo_sale.object', {
#             'object': obj
#         })

