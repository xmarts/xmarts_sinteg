# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions,_
from datetime import datetime, date, time, timedelta
import calendar 
from openerp.exceptions import UserError, RedirectWarning, ValidationError
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_compare
from odoo.tools.misc import formatLang
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
    provider_id = fields.Many2one("res.partner", string="Proveedor", domain=[('supplier', '=', True)])
    product_price = fields.Float(string="Precio Unitario")
    subtotal = fields.Float(string="Subtotal", compute="_calc_subtotal")
    purr_id = fields.Many2one("purchase.order.request")
    product_taxes = fields.Many2many("account.tax", default=lambda self: self.env['account.tax'].search([('name', '=', ['IVA(16%) COMPRAS'])]).ids , string="Impuestos")
    estatus= fields.Selection(selection=[('ace', 'Aceptado'),('pen', 'Pendiente'),('cot','Cotizado'),('can','Cancelado')],string='Estado', default="ace")
    
    #price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
    #price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)

    order_id = fields.Many2one('purchase.order.request', string='Order Reference', index=True, required=True, ondelete='cascade')
   
    
    @api.depends('product_qty', 'product_price', 'product_taxes')
    def _compute_amount(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            taxes = line.product_taxes.compute_all(
                vals['product_price'],
                vals['currency_id'],
                vals['product_qty'],
                vals['product'],
                #vals['partner']
                )
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                #'price_total': taxes['total_included'],
                #'price_subtotal': taxes['total_excluded'],
            })

    def _prepare_compute_all_values(self):
        # Hook method to returns the different argument values for the
        # compute_all method, due to the fact that discounts mechanism
        # is not implemented yet on the purchase orders.
        # This method should disappear as soon as this feature is
        # also introduced like in the sales module.
        self.ensure_one()
        return {
            'product_price': self.product_price,
            'currency_id': self.order_id.currency_id,
            'product_qty': self.product_qty,
            'product': self.product_id,
            #'partner': self.order_id.tickets.partner_id.id,
        }  
    
    @api.onchange('product_price')
    def onchange_estatus(self):
        if self.product_price > 8000:
            self.estatus='pen'
        if self.product_price <= 8000:
            self.estatus='ace'

        
 
        
    @api.multi
    def est(self):
        self.estatus='ace'

    @api.multi
    def estado(self):
        self.estatus='can'
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        self.name = self.product_id.name
        self.provider_id = None

    @api.one
    @api.depends('product_qty', 'product_price')
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
    company_ids = fields.Many2one("res.company", related="create_uid.company_id")
    currency_id = fields.Many2one("res.currency", related="company_ids.currency_id")

    message_follower_ids = fields.One2many("mail.followers", "res_id")
    activity_ids = fields.One2many("mail.activity", "res_id")
    message_ids = fields.One2many("mail.message", "res_id")

    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')
    estado_solicitud= fields.Selection(selection=[('ace', 'Aceptado'),('pen', 'Pendiente'),('can','Cancelado')],string='Estado de Solicitud', default="ace")

    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.user.company_id.id)
    ocultar=fields.Boolean(string='ocultar campo',compute="_compute_campo")

    @api.depends()
    def _compute_campo(self):
        cont=0
        for l in self.request_lines:
            if l.estatus=='pen':
                cont+=1
        if cont>0:
            self.ocultar=True

    @api.depends('request_lines.product_price')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.request_lines:
                amount_untaxed += line.subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })


    @api.multi
    def state_request(self):
        if self.request_lines:
            self.request_date = datetime.now()
            self.state = 'request'
        else:
            raise exceptions.ValidationError('No hay lineas cargadas')

    @api.multi
    @api.model
    def state_done(self,vals):


        lista_part = []
        for l in self.request_lines:
            if not l.provider_id:
                raise exceptions.ValidationError('Existen lineas sin proveedor asignado')
            if l.provider_id.id not in lista_part:
                lista_part.append(l.provider_id.id)

        cont=0
        for l in self.request_lines:
            if l.estatus=='pen':
                cont+=1


        now = datetime.now()
        if cont > 0:
            self.ocultar=True
                    
        if cont ==0:
            for p in lista_part:

                purchase_objs = self.env["purchase.order"]
                purchase_line_objs = self.env["purchase.order.line"]

                curr_orders = {
                    'name':  self.env['ir.sequence'].next_by_code('purchase.order'),
                    'company_id': self.company_id.id,
                    'currency_id': self.currency_id.id,
                    'date_order': datetime.now(),
                    'partner_id': p,
                    'origin': self.name,
                    'tickets': self.tickets.id,
                    'state': 'draft'
                }

                ord_ids = purchase_objs.create(curr_orders)
                ord_id = ord_ids.id
               
                if ord_ids:
                    for pl in self.request_lines:
                        if pl.estatus=='ace':                                    
                            if pl.provider_id.id == p:
                                taxes = []
                                for t in pl.product_taxes:
                                    taxes.append(t.id)
                             
                                curr_order_lines = {
                                    'order_id': ord_id,
                                    'name': pl.name,
                                    'price_unit': pl.product_price,
                                    'product_id': pl.product_id.id,
                                    'product_qty': pl.product_qty,
                                    'product_uom': pl.product_id.uom_id.id,
                                    'order_id': ord_id,
                                    'taxes_id': [(6, 0, taxes)],
                                    'date_planned': now.strftime('%Y-%m-%d 06:00:00'),
                                    'tickets':self.tickets.id,

                                }
                                pl.estatus='cot'

                            pur_line_ids = purchase_line_objs.create(curr_order_lines)
            self.done_date = datetime.now()
            self.state = 'done'
            self.estado_solicitud='ace' 

    @api.multi
    def state_cancel(self):
        self.request_date = ''
        self.done_date = ''
        self.state = 'cancel'
        self.estado_solicitud='can'

    @api.multi
    def state_draft(self):
        self.state = 'draft'


    @api.one
    @api.model
    def notificar_logistica(self):
        activity_obj = self.env['mail.activity']
        sale_model = self.env['ir.model'].search([('model','=','purchase.order.request')],limit=1)
        users_l = self.env['res.users'].search([('name','=','Administrator')])
        for u in users_l:
            today = date.today()
            activity_values = {
                'res_id': self.id,
                'res_model_id': sale_model.id,
                'res_model': 'purchase.order.request',
                'date_deadline': today,
                'user_id': u.id,
                'note': 'Validación de la solicitud de Compra '+str(self.name)+'.'
            }
            activity_id = activity_obj.create(activity_values)
            if activity_id:
                    self.estado_solicitud='pen'
                    self.message_post(body="Solicitud enviada para aprobacion")

    @api.multi
    def action_rfq_send(self):
        '''
        This function opens a window to compose an email, with the edi purchase template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        template = self.env.ref('xmarts_order_request.email_purchase_solicitud', False)
        
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'purchase.order.request',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template),
            'default_template_id': template and template.id or False,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'mark_rfq_as_sent': True,
        })


        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }




class AccountInvoiceConfirm(models.TransientModel):
    """
    This wizard will confirm the all the selected draft invoices
    """

    _name = "purchase.order.confirm"
    _description = "Confirm the selected invoices"

    @api.multi
    def invoice_confirm(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for record in self.env['purchase.order'].browse(active_ids):
                       
            for order in record:

                if order.state not in ['draft', 'sent']:
                    continue
                order._add_supplier_to_product()
                # Deal with double validation process
                if order.company_id.po_double_validation == 'one_step'\
                        or (order.company_id.po_double_validation == 'two_step'\
                            and order.amount_total < self.env.user.company_id.currency_id._convert(
                                order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                        or order.user_has_groups('purchase.group_purchase_manager'):
                    order.button_approve()
                else:
                    order.write({'state': 'to approve'})
                
        return {'type': 'ir.actions.act_window_close'}
