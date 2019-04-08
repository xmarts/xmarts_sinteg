# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.float_utils import float_compare
from openerp.exceptions import UserError, RedirectWarning, ValidationError


class ResPartner(models.Model):
	_inherit = ['res.partner']

	name=fields.Char(track_visibility='onchange')
	street=fields.Char(track_visibility='onchange')
	street2=fields.Char(track_visibility='onchange')
	city=fields.Char(track_visibility='onchange')
	state_id=fields.Many2one(track_visibility='onchange')
	zip=fields.Char(track_visibility='onchange')
	country_id=fields.Many2one(track_visibility='onchange')

	vat=fields.Char(track_visibility='onchange')
	function=fields.Char(track_visibility='onchange')
	phone=fields.Char(track_visibility='onchange')
	mobile=fields.Char(track_visibility='onchange')
	email=fields.Char(track_visibility='onchange')
	website=fields.Char(track_visibility='onchange')
	title=fields.Many2one(track_visibility='onchange')
	lang=fields.Selection(track_visibility='onchange')
	category_id=fields.Many2many(track_visibility='onchange')
	#contacs & address
	#child_id=fields.One2many(track_visibility='onchange')
	#Sales & Purchases
	customer=fields.Boolean(track_visibility='onchange')
	user_id=fields.Many2one(track_visibility='onchange')
	property_delivery_carrier_id=fields.Many2one(track_visibility='onchange')
	message_bounce=fields.Integer(track_visibility='onchange')
	property_payment_term_id=fields.Many2one(track_visibility='onchange')
	ref=fields.Char(track_visibility='onchange')
	barcode=fields.Char(track_visibility='onchange')
	company_id=fields.Many2one(track_visibility='onchange')
	property_stock_customer=fields.Many2one(track_visibility='onchange')
	property_stock_supplier=fields.Many2one(track_visibility='onchange')
	supplier=fields.Boolean(track_visibility='onchange')
	property_supplier_payment_term_id=fields.Many2one(track_visibility='onchange')
	property_account_position_id=fields.Many2one(track_visibility='onchange')

	_sql_constraints = [(
		'default_code_unique',
		'unique(email)',
		'El correo ya existe, favor de modificarlo'
		)]

class Marca(models.Model):
	_name = 'claim.marca'
	name=fields.Char(string='Nombre')



class Modelo(models.Model):
	_name = 'claim.modelo'
	name=fields.Char(string='Nombre')

class claim_picking(models.Model):
	_inherit ='crm.claim.ept'
	picking_id=fields.Many2one('stock.picking' , string='Delivery Order')

	@api.onchange('picking_id')
	def onchange_picking_id(self):
		if self.picking_id:
			self.partner_id = self.picking_id.partner_id.id
			self.partner_phone = self.picking_id.partner_id.phone
			self.email_from = self.picking_id.partner_id.email
			self.sale_id = self.picking_id.sale_id.id
			claim_lines = [
				(0, 0, {'product_id': move.product_id.id,'marca': move.marca.id, 'modelo':move.modelo.id, 'series':move.series,'observaciones':move.observaciones, 'quantity': move.product_uom_qty, 'move_id': move.id}) for
				move in self.picking_id.move_lines]
			self.claim_line_ids = claim_lines

	@api.onchange('partner_id')
	def onchange_partner_id(self):
		if self.partner_id:
			self.partner_phone = self.partner_id.phone
			self.email_from = self.partner_id.email

	# @api.multi
	# def create_tiket(self, amount, commission, type, factura):
	# 	commission_obj = self.env['sales.commission.line']
	# 	product = self.env['product.product'].search([('is_commission_product','=',1)],limit=1)
	# 	for vivienda in self:
	# 		if amount != 0.0:
	# 			commission_value = {
	# 			# 'sales_team_id': invoice.team_id.id,
	# 				'commission_user_id': vivienda.asesor.id,
	# 				'amount': amount,
	# 				'amount_company_currency': amount,
	# 				'origin': vivienda.name,
	# 				'type':type,
	# 				'product_id': product.id,
	# 				'date' : datetime.now(),
	# 				'src_invoice_id': factura,
	# 				'sales_commission_id':commission.id,
	# 			}
	# 			commission_id = commission_obj.create(commission_value)
	# 			if type == 'sales_person':
	# 				vivienda.commission_person_id = commission_id.id
	# 	return True


class claim(models.Model):
	_inherit ='claim.line.ept'
#	equipo = fields.Char(string='Equipo')
	marca = fields.Many2one('claim.marca',string='Marca')
	modelo = fields.Many2one('claim.modelo', string='Modelo')
	series = fields.Char(string='Series')
	observaciones=fields.Text(string='Observaciones')










	

class claim_product(models.Model):
	_inherit ='product.template'
#	equipo = fields.Char(string='Equipo')
	marca = fields.Many2one('claim.marca', string='Marca')
	modelo = fields.Many2one('claim.modelo', string='Modelo')
	series = fields.Char(string='Series')
	observaciones=fields.Text(string='Observaciones')

class claim(models.Model):
	_inherit ='product.product'
	marca = fields.Many2one(related='product_tmpl_id.marca',string='marca')
	modelo = fields.Many2one(related='product_tmpl_id.modelo',string='modelo')

class claim_product(models.Model):
	_inherit ='stock.move'
#	equipo = fields.Char(string='Equipo')
	marca = fields.Many2one('claim.marca', string='Marca' )
	modelo = fields.Many2one('claim.modelo', string='Modelo')
	sub_modelo=fields.Many2one('helpdesk.sub_modelo',string='Sub Modelo')
	series = fields.Char(string='Series')
	observaciones=fields.Text(string='Observaciones')
	tickets=fields.Many2one('helpdesk.support',string='Ticket', readonly=True)


class product_product(models.Model):
	_inherit ='product.product'
#	equipo = fields.Char(string='Equipo')
	marca = fields.Many2one('claim.marca', string='Marca')
	modelo = fields.Many2one('claim.modelo', string='Modelo')
	series = fields.Char(string='Series')
	observaciones=fields.Text(string='Observaciones')

# class tipo_contrato(models.Model):
# 	_name = 'helpdesk.tipo.contrato'
# 	name=fields.Char(string='Nombre')

# class equip(models.Model):
# 	_name = 'helpdesk.equipos.contrato'
# 	name=fields.Char(string='Nombre')

class Modelo(models.Model):
	_name = 'helpdesk.sub_modelo'
	name=fields.Char(string='Nombre')


class helpdesk_ticket(models.Model):
	_inherit ='helpdesk.support'

	contrato = fields.Boolean(string='Contrato')
	# equipo_contrato = fields.Many2one('claim.modelo', string='Equipos de Contrato')
	tipo_ticket= fields.Selection(selection=[('CARGO', 'cargo'),('GARANTIA', 'garantia'),
											 ('SERVICIO', 'servicio'),('CONTRATO', 'contrato'),
											 ('INTERNO', 'interno'),('VENTA', 'venta'),
											 ('CALIDAD', 'calidad'),('MAIP', 'ma ip'),
											 ('MAGOB', 'ma gob'),
											 ('SG', 'sg')],string='Tipo de Ticket',default='CARGO', required=True)

	tipo= fields.Selection(selection=[('entregar_cli', 'Entregar Cliente'),
									  ('recoleccion_cli', 'Recoleccion Cliente'),
									  ('recoleccion_pro', 'Recoleccion Proveedor'),
									  ('entregar_pro', 'Entregar Proveedor'),
									  ('traslado_per', 'Traslado de Personal'),
									  ('recoger_doc ', 'Recoger Documentos '),
									  ('entregar_doc', 'Entregar Documentos'),
									  ('entrega_rec', 'Entrega y Recoleccion'),
									  ('recoleccion_ent', 'Recoleccion y Entrega')],string='Tipo',default='entregar_cli')

		
	solicitante=fields.Char(string='Solicitante')
	marca = fields.Many2one('claim.marca', string='Marca')
	modelo = fields.Many2one('claim.modelo', string='Modelo')
	series = fields.Char(string='Series')
	observaciones=fields.Text(string='Observaciones Adicionales')
	doc_c = fields.Binary(string='Documento')
	product_id=fields.Many2one('product.product',string='Producto')
	picking_type_id=fields.Many2one('stock.picking.type',string='Tipo de Operación')
	location_dest_id=fields.Many2one('stock.location',string='Ubicación destino')
	location_id = fields.Many2one('stock.location', 'Return Location')

	
	@api.onchange('team_id')
	def _onchange_location_dest_id(self):
		self.picking_type_id =self.team_id.picking_type_id.id
		self.location_dest_id = self.picking_type_id.default_location_dest_id.id

		self.location_id = self.picking_type_id.default_location_src_id.id


	sub_modelo=fields.Many2one('helpdesk.sub_modelo',string='Sub Modelo')
	falla=fields.Char(string='Falla Reportada')
	des_solicitud=fields.Text(string='Descripción de la Solicitud')
	contacto=fields.Char(string='Contacto')
	descripcion=fields.Text(string='Descripción')
	cantidad=fields.Integer(string='Cantidad')
	garantia=fields.Boolean(string='cuenta con garantía')
	uom_name=fields.Char(string='uom')
	sal =fields.Boolean(string='salida')
	# or 'SERVICIO' or 'CONTRATO' or 'MAIP' or 'MAGOB'
	#stock=fields.Many2one('stock.move.tickets')
	current_user_id = fields.Many2one(
	comodel_name='res.users',
	string='Usuario Actual',
	default=lambda self: self.env.uid
	)

	

	acce = fields.One2many(
		'purchase.order.line',
		'tickets',
		string='',
		readonly=True,
	)




	@api.multi
	def show_ticket(self):
		for rec in self:
			res = self.env.ref('purchase.purchase_order_form')
			res = res.read()[0]
			res['domain'] = str([('tickets','=',rec.id)])
		return res	
	
	@api.model
	def _default_current_user_id(self):
		return self.env.uid

	@api.onchange('product_id')
	def oum_product(self):
		if self.product_id:
			self.uom_name=self.product_id.uom_id.id
		
	
	@api.model
	def create(self, vals):
		if vals.get('name', False):
			if vals.get('name', 'New') != 'New':
				vals['subject'] = vals['name']
				vals['name'] = 'New'
		if vals.get('name', 'New') == 'New':
			vals['name'] = self.env['ir.sequence'].next_by_code('helpdesk.support') or 'New'

			# tipo_ticket = vals.get("tipo_ticket")

			# if (tipo_ticket == 'GARANTIA') or  (tipo_ticket == 'INTERNO') or  (tipo_ticket == 'CARGO') or  (tipo_ticket == 'SERVICIO') or (tipo_ticket == 'CONTRATO') or  (tipo_ticket == 'MAIP') or  (tipo_ticket == 'MAGOB'): 
			# 	inv_obj = self.env['stock.picking']
			# 	move_line_obj = self.env['stock.move']
			# 	product_obj=self.env['product.product']

			# 	ticket = vals.get("name")
			# 	partner = vals.get("partner_id")
			# 	location = vals.get("location_id")
			# 	picking_type = vals.get("picking_type_id")
			# 	location_dest = vals.get("location_dest_id")
				
			# 	v=1
			# 	invoice ={
					
			# 	    'partner_id': partner,
			# 		'location_id':location,
			# 		'picking_type_id':picking_type,
			# 		'location_dest_id':location_dest,
			# 		'ticket':ticket,
					
			# 		'state':'assigned',
			# 		'p':str(vals.get('uom_name'))

			# 	}
			# 	inv_ids = inv_obj.create(invoice)
			# 	inv_id=inv_ids.id

			# 	name = vals.get("name")
			# 	product_ids = vals.get("product_id")
			# 	marca = vals.get("marca")
			# 	modelo = vals.get("modelo")
			# 	sub_modelo = vals.get("sub_modelo")			
			# 	series = vals.get("series")
			# 	observaciones = vals.get("observaciones")
			# 	product_uom = vals.get("product_id")			
			# 	location_id = vals.get("location_id")

			# 	location_dest_id = vals.get("location_dest_id")

			# 	if inv_id:
			# 		move_line={
			# 		'picking_id':inv_id,
			# 		'name':name,
			# 		'product_id':product_ids,
			# 		'marca': marca,
			# 		'modelo': modelo,
			# 		'sub_modelo': sub_modelo,
			# 		'series': series,
			# 		'observaciones':observaciones,
			# 		'picking_type_code':'outgoing',
			# 		'product_uom_qty': '0.00',
			# 		'reserved_availability': '0.00',
			# 		'quantity_done':'0.00',
			# 		'product_uom':str(vals.get('uom_name')),
			# 		'product_uom_id':str(vals.get('uom_name')),
			# 		'location_id':location_id,
			# 		'location_dest_id':location_dest_id,
			# 		'state':'confirmed'
					
			# 		}
			# 		move_ids_without_package=move_line_obj.create(move_line)

	
		# set up context used to find the lead's sales team which is needed
		# to correctly set the default stage_id
		context = dict(self._context or {})
		if vals.get('type') and not self._context.get('default_type'):
			context['default_type'] = vals.get('type')
		if vals.get('team_id') and not self._context.get('default_team_id'):
			context['default_team_id'] = vals.get('team_id')

		if not vals.get('partner_id', False) and vals.get('email', ''):
			partner = self.env['res.partner'].sudo().search([('email', '=', vals['email'])], limit=1)
			if partner:
				vals.update({'partner_id': partner.id})

		if vals.get('team_id') and not vals.get('team_leader_id'):
			vals['team_leader_id'] = self.env['support.team'].browse(vals.get('team_id')).leader_id.id

		# context: no_log, because subtype already handle this
		res = super(helpdesk_ticket, self.with_context(context, mail_create_nolog=True)).create(vals)

		if res:

			tipo_ticket = vals.get("tipo_ticket")

			if (tipo_ticket == 'GARANTIA') or  (tipo_ticket == 'INTERNO') or  (tipo_ticket == 'CARGO') or  (tipo_ticket == 'SERVICIO') or (tipo_ticket == 'CONTRATO') or  (tipo_ticket == 'MAIP') or  (tipo_ticket == 'MAGOB'): 
			
				
				product_obj=self.env['product.product']

				ticket = vals.get("name")
				partner = vals.get("partner_id")
				location = vals.get("location_id")
				picking_type = vals.get("picking_type_id")
				location_dest = vals.get("location_dest_id")
				name = vals.get("name")
				product_ids = vals.get("product_id")
				marca = vals.get("marca")
				modelo = vals.get("modelo")
				sub_modelo = vals.get("sub_modelo")			
				series = vals.get("series")
				observaciones = vals.get("observaciones")
				product_uom = vals.get("product_id")			
				location_id = vals.get("location_id")
				location_dest_id = vals.get("location_dest_id")
				company = vals.get("company_id")


				do=self.env['stock.picking'].create({'partner_id':partner,'location_id':location,'location_dest_id':location_dest,'picking_type_id':picking_type,'tickets':res.id,'p':str(vals.get('uom_name'))})
				

				self.env['stock.move'].create({         
					'location_id':location,
					'location_dest_id':location_dest,
					'product_uom_qty':'1',
					'name':name,
					'product_id':product_ids,
					'state':'draft',
					'marca': marca,
					'modelo': modelo,
					'sub_modelo': sub_modelo,
					'series': series,
					'observaciones':observaciones,						
					'picking_id':do.id,
					'product_uom':str(vals.get('uom_name')),
					#'company_id': company
				})
				do.action_assign()
		

		return res
	



	@api.model
	def _create_apple_dos(self):
		inv_obj = self.env['stock.picking']
		move_line_obj = self.env['stock.move']
		self.ensure_one()
		cr = self.env.cr
		sql ="select id from helpdesk_support where name='"+str(self.name)+"' limit 1"
		cr.execute(sql)
		id_ticket = cr.fetchone()
		ticket=id_ticket[0]
		entrada =self.env['stock.picking']
		lines = entrada.search([('tickets', '=', ticket)])
		
		if lines:
			for l in lines:

				if l.state =='done':

					
					do=self.env['stock.picking'].create({
						'partner_id':self.partner_id.id,
						'location_id':l.location_dest_id .id,
						'location_dest_id':l.location_id.id,	
						'picking_type_id':2,
						'origin':l.origin,
						'tickets':l.tickets.id,										
						'picking_type_code':'outgoing',
						'state':'draft',
						'origin':self.name})
						
					if do:
						for li in l.move_ids_without_package:

							self.env['stock.move'].create({

							'picking_id':do.id,
							'name':li.name,
							'product_id':li.product_id.id,
							'marca':  li.marca.id,
							'modelo': li.modelo.id,
							'sub_modelo': li.sub_modelo.id,
							'series': li.series,
							'observaciones': li.observaciones,
							'picking_type_code':'outgoing',
							'picking_type_id':2,
							'product_uom_qty': li.product_uom_qty,
							'reserved_availability': li.reserved_availability,
							#'quantity_done':li.quantity_done,
							'product_uom':li.product_id.uom_id.id,
							'product_uom_id':'1',
							'location_id':li.location_dest_id.id,
							'location_dest_id':li.location_id.id,
							'state':'draft'
							})
     
							do.action_assign()
							self.sal=True

				else:
					raise UserError('No se a ingresado equipo al almacen ')
				
					return invoice


	def create_apple_dos(self):
		self._create_apple_dos()

	@api.multi
	def compras(self, cr,  context=None):
		inv_obj_compras = self.env['purchase.order.request']
		#compra_id=self.browse(cr, uid, ids[0], context)['compra_id']
		#view_ref=self.pool.get('ir.model.data').get_object_reference(cr, uid,'xmarts_order_request','purchase_order_request_view_form')
		
		#view_id =view_ref and view_ref[1] or False
		cr = self.env.cr
		sql ="select id from helpdesk_support where name='"+str(self.name)+"' limit 1"
		cr.execute(sql)
		id_ticket = cr.fetchone()
		ticket=id_ticket[0]
		orden =self.env['purchase.order.request']
		ordens = orden.search([('tickets', '=', ticket)],limit=1)
		ids=ordens.id
		if not ids:
			invoice_c ={
					
				'tickets': ticket,
				'state':'draft'
			}
			inv_ids = inv_obj_compras.create(invoice_c)
			
			return {
				'type': 'ir.actions.act_window',
				'res_model': 'purchase.order.request',
				'view_mode': 'form',
				'res_id': inv_ids.id,
				'target': 'current',
				'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}}
				}
		elif ids:

			return {
				'type': 'ir.actions.act_window',
				'res_model': 'purchase.order.request',
				'view_mode': 'form',
				'res_id': ids,
				'target': 'current',
				'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}}
				}
		



class PurchaseOrder(models.Model):
	_inherit = 'purchase.order.request'

	tickets=fields.Many2one('helpdesk.support',string='Ticket', readonly=True)
	ticket=fields.Char(string='Ticket', readonly=True)

class PurchaseOrder(models.Model):
	_inherit = 'purchase.order'

	tickets=fields.Many2one('helpdesk.support',string='Ticket', readonly=True)
	

	@api.model
	def _prepare_picking(self):
		if not self.group_id:
			self.group_id = self.group_id.create({
				'name': self.name,
				'partner_id': self.partner_id.id
			})
		if not self.partner_id.property_stock_supplier.id:
			raise UserError(_("You must set a Vendor Location for this partner %s") % self.partner_id.name)
		return {
			'picking_type_id': self.picking_type_id.id,
			'partner_id': self.partner_id.id,
			'date': self.date_order,
			'origin': self.name,
			'location_dest_id': self._get_destination_location(),
			'location_id': self.partner_id.property_stock_supplier.id,
			'tickets': self.tickets.id,
			'company_id': self.company_id.id,
		}

class PurchaseOrderLine(models.Model):
	_inherit = 'purchase.order.line'

	tickets=fields.Many2one('helpdesk.support',string='Ticket', readonly=True)

	@api.multi
	def _prepare_stock_moves(self, picking):
		""" Prepare the stock moves data for one order line. This function returns a list of
		dictionary ready to be used in stock.move's create()
		"""
		self.ensure_one()
		res = []
		if self.product_id.type not in ['product', 'consu']:
			return res
		qty = 0.0
		price_unit = self._get_stock_move_price_unit()
		for move in self.move_ids.filtered(lambda x: x.state != 'cancel' and not x.location_dest_id.usage == "supplier"):
			qty += move.product_uom._compute_quantity(move.product_uom_qty, self.product_uom, rounding_method='HALF-UP')
		
		ticket =self.env['purchase.order']
		origin = ticket.search([('origin', '=', self.order_id.name)],limit=1)
		id_tickets=origin.tickets

		template = {
			'name': self.name or '',
			'product_id': self.product_id.id,
			'product_uom': self.product_uom.id,
			'date': self.order_id.date_order,
			'date_expected': self.date_planned,
			'location_id': self.order_id.partner_id.property_stock_supplier.id,
			'location_dest_id': self.order_id._get_destination_location(),
			'picking_id': picking.id,
			'partner_id': self.order_id.dest_address_id.id,
			'move_dest_ids': [(4, x) for x in self.move_dest_ids.ids],
			'state': 'draft',
			'purchase_line_id': self.id,
			'company_id': self.order_id.company_id.id,
			'price_unit': price_unit,
			'picking_type_id': self.order_id.picking_type_id.id,
			'group_id': self.order_id.group_id.id,
			'origin': self.order_id.name,
			'tickets': self.tickets.id,
			'route_ids': self.order_id.picking_type_id.warehouse_id and [(6, 0, [x.id for x in self.order_id.picking_type_id.warehouse_id.route_ids])] or [],
			'warehouse_id': self.order_id.picking_type_id.warehouse_id.id,
		}
		diff_quantity = self.product_qty - qty
		if float_compare(diff_quantity, 0.0,  precision_rounding=self.product_uom.rounding) > 0:
			quant_uom = self.product_id.uom_id
			get_param = self.env['ir.config_parameter'].sudo().get_param
			if self.product_uom.id != quant_uom.id and get_param('stock.propagate_uom') != '1':
				product_qty = self.product_uom._compute_quantity(diff_quantity, quant_uom, rounding_method='HALF-UP')
				template['product_uom'] = quant_uom.id
				template['product_uom_qty'] = product_qty
			else:
				template['product_uom_qty'] = diff_quantity
			res.append(template)
		return res

	# @api.multi
	# def _create_or_update_picking(self,vals):
	# 	for line in self:
	# 		if line.product_id.type in ('product', 'consu'):
	# 			# Prevent decreasing below received quantity
	# 			if float_compare(line.product_qty, line.qty_received, line.product_uom.rounding) < 0:
	# 				raise UserError(_('You cannot decrease the ordered quantity below the received quantity.\n'
	# 								 'Create a return first.'))

	# 			if float_compare(line.product_qty, line.qty_invoiced, line.product_uom.rounding) == -1:
	# 				# If the quantity is now below the invoiced quantity, create an activity on the vendor bill
	# 				# inviting the user to create a refund.
	# 				activity = self.env['mail.activity'].sudo().create({
	# 					'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
	# 					'note': _('The quantities on your purchase order indicate less than billed. You should ask for a refund. '),
	# 					'res_id': line.invoice_lines[0].invoice_id.id,
	# 					'res_model_id': self.env.ref('account.model_account_invoice').id,
	# 				})
	# 				activity._onchange_activity_type_id()

	# 			# If the user increased quantity of existing line or created a new line
	# 			pickings = line.order_id.picking_ids.filtered(lambda x: x.state not in ('done', 'cancel') and x.location_dest_id.usage in ('internal', 'transit'))
	# 			picking = pickings and pickings[0] or False
	# 			if not picking:
	# 				res = line.order_id._prepare_picking()
	# 				picking = self.env['stock.picking'].create(res)
	# 			move_vals = line._prepare_stock_moves(picking,vals)
	# 			for move_val in move_vals:
	# 				self.env['stock.move']\
	# 					.create(move_val)\
	# 					._action_confirm()\
	# 					._action_assign()

	# @api.multi
	# def _create_stock_moves(self, picking, vals):
	# 	moves = self.env['stock.move']
	# 	done = self.env['stock.move'].browse()
	# 	for line in self:
	# 		for val in line._prepare_stock_moves(picking,vals):
	# 			done += moves.create(val)
	# 	return done


class stockpicking(models.Model):
	_inherit = 'stock.picking'


	ticket=fields.Char(string='Ticket', readonly=True)
	tickets=fields.Many2one('helpdesk.support',string='Ticket', readonly=True)


class stockpicking(models.Model):
	_inherit = 'res.partner'


	rfc=fields.Char(string='RFC')
	colonia=fields.Char(string='Colonia')
	municipio=fields.Char(string='Municipio')
	estado=fields.Char(string='Estado')
	referencia=fields.Char(string='Referencia')


