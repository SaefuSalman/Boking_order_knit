# -*- coding: utf-8 -*-
# from odoo import http


# class BookingOrderSaefuSalman(http.Controller):
#     @http.route('/booking_order_saefu_salman/booking_order_saefu_salman/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/booking_order_saefu_salman/booking_order_saefu_salman/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('booking_order_saefu_salman.listing', {
#             'root': '/booking_order_saefu_salman/booking_order_saefu_salman',
#             'objects': http.request.env['booking_order_saefu_salman.booking_order_saefu_salman'].search([]),
#         })

#     @http.route('/booking_order_saefu_salman/booking_order_saefu_salman/objects/<model("booking_order_saefu_salman.booking_order_saefu_salman"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('booking_order_saefu_salman.object', {
#             'object': obj
#         })
