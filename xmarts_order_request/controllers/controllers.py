# -*- coding: utf-8 -*-
from odoo import http

# class XmartsOrderRequest(http.Controller):
#     @http.route('/xmarts_order_request/xmarts_order_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/xmarts_order_request/xmarts_order_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('xmarts_order_request.listing', {
#             'root': '/xmarts_order_request/xmarts_order_request',
#             'objects': http.request.env['xmarts_order_request.xmarts_order_request'].search([]),
#         })

#     @http.route('/xmarts_order_request/xmarts_order_request/objects/<model("xmarts_order_request.xmarts_order_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('xmarts_order_request.object', {
#             'object': obj
#         })