# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions,_
from datetime import datetime, date, time, timedelta
import calendar 

# class xmarts_order_request(models.Model):
#     _name = 'xmarts_order_request.xmarts_order_request'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class PurchaseOrderRequestLines(models.Model):
    _name = "purchase.order.request.line"
    _description = 'Lineas de solicitud de compra'

    product_id = fields.Many2one("product.product", string="producto", required=True)
    product_template_id = fields.Many2one("product.template", related="product_id.product_tmpl_id")    
    name = fields.Char(string="Descripcion", required=True)
    product_qty = fields.Float(string="Cantidad", default=1.0)
    provider_id = fields.Many2one("product.supplierinfo", string="Proveedor")
    product_price = fields.Float(string="Precio Unitario", related="provider_id.price", readonly=True)
    product_taxes = fields.Many2many("account.tax", string="Impuestos", related="product_id.supplier_taxes_id", readonly=True)
    subtotal = fields.Float(string="Subtotal", compute="_calc_subtotal")
    purr_id = fields.Many2one("purchase.order.request")


    @api.onchange('product_id')
    def onchange_product_id(self):
        self.name = self.product_id.name
        self.provider_id = None

    @api.one
    def _calc_subtotal(self):
        self.subtotal = self.product_qty * self.product_price

    # @api.onchange('product_id')
    # def onchange_product_id(self):
    #     self.name = self.product_id.name
    #     self.provider_id = None
    #     lista = []
    #     res = {}
    #     cr = self.env.cr
    #     if self.product_id.id != False:
    #         sql = "select id from product_supplierinfo where product_tmpl_id='"+str(self.product_id.product_tmpl_id.id)+"';"
    #         cr.execute(str(sql))
    #         provs = cr.fetchall()
    #         if provs != None:
    #             provedores = []
    #             for l in provs:
    #                 provedores.append(l[0])
    #             res.update({
    #                 'domain': {
    #                     'provider_id': [('id', 'in', list(set(provedores)))],
    #                 }
    #             })
    #     return res

    

class PurchaseOrderRequest(models.Model):
    _name = "purchase.order.request"
    _description = 'Solicitud de compra'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    @api.model
    def create(self, vals):
        cr = self.env.cr
        cr.execute('select coalesce(max(id), 0) from "purchase_order_request"')
        id_returned = cr.fetchone()
        if (max(id_returned)+1) < 10:
            vals['name'] = "Orden Nº 00" + str(max(id_returned)+1)
        if (max(id_returned)+1) >= 10 and (max(id_returned)+1) < 100:
            vals['name'] = "Orden Nº 0" + str(max(id_returned)+1)
        if (max(id_returned)+1) >= 100 :
            vals['name'] = "Orden Nº " + str(max(id_returned)+1)
        result = super(PurchaseOrderRequest, self).create(vals)
        return result


    state = fields.Selection([('draft','Borrador'),('request','Solicitada'),('done','Pedido realizado'),('cancel','Cancelada')], string="Status", default='draft', track_visibility='onchange')
    name = fields.Char(string="Solicitud", readonly=True, track_visibility='onchange')
    request_lines = fields.One2many("purchase.order.request.line", "purr_id", string="Lineas de solicitud")
    request_date = fields.Datetime(string="Fecha de solicitud", readonly=True, track_visibility='onchange')
    done_date = fields.Datetime(string="Fecha de orden", readonly=True, track_visibility='onchange')
    company_id = fields.Many2one("res.company", related="create_uid.company_id")
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id")

    message_follower_ids = fields.One2many("mail.followers", "res_id")
    activity_ids = fields.One2many("mail.activity", "res_id")
    message_ids = fields.One2many("mail.message", "res_id")


    @api.multi
    def state_request(self):
        if self.request_lines:
            self.request_date = datetime.now()
            self.state = 'request'
        else:
            raise exceptions.ValidationError('No hay lineas cargadas')

    @api.multi
    @api.model
    def state_done(self):


        lista_part = []
        for l in self.request_lines:
            if not l.provider_id:
                raise exceptions.ValidationError('Existen lineas sin proveedor asignado')
            if l.provider_id.name.id not in lista_part:
                lista_part.append(l.provider_id.name.id)

        now = datetime.now()
        for p in lista_part:

            purchase_obj = self.env["purchase.order"]
            purchase_line_obj = self.env["purchase.order.line"]

            curr_order = {
                'name':  self.env['ir.sequence'].next_by_code('purchase.order'),
                'company_id': self.company_id.id,
                'currency_id': self.currency_id.id,
                'date_order': datetime.now(),
                'partner_id': p,
                'origin': self.name,
                'state': 'purchase'
            }

            ord_ids = purchase_obj.create(curr_order)
            ord_id = ord_ids.id

            if ord_ids:
                for pl in self.request_lines:
                    if pl.provider_id.name.id == p:
                        taxes = []
                        for t in pl.product_taxes:
                            taxes.append(t.id)
                        curr_order_line = {
                            'order_id': ord_id,
                            'name': pl.name,
                            'price_unit': pl.product_price,
                            'product_id': pl.product_id.id,
                            'product_qty': pl.product_qty,
                            'product_uom': pl.product_id.uom_id.id,
                            'order_id': ord_id,
                            'taxes_id': [(6, 0, taxes)],
                            'date_planned': now.strftime('%Y-%m-%d 06:00:00'),
                        }

                        pur_line_ids = purchase_line_obj.create(curr_order_line)
        self.done_date = datetime.now()
        self.state = 'done'

    @api.multi
    def state_cancel(self):
        self.request_date = ''
        self.done_date = ''
        self.state = 'cancel'

    @api.multi
    def state_draft(self):
        self.state = 'draft'