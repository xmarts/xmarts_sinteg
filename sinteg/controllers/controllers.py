# -*- coding: utf-8 -*-
from odoo import http

# class Sinteg(http.Controller):
#     @http.route('/sinteg/sinteg/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sinteg/sinteg/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sinteg.listing', {
#             'root': '/sinteg/sinteg',
#             'objects': http.request.env['sinteg.sinteg'].search([]),
#         })

#     @http.route('/sinteg/sinteg/objects/<model("sinteg.sinteg"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sinteg.object', {
#             'object': obj
#         })