import logging

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

TERMINO_PAGO_SELECTION = [
    ('contado', 'Al contado'),
    ('plazo_15', '15 días plazo'),
    ('plazo_30', '30 días plazo')
]

STATE_SELECTION = [
    ('budget', 'Presupuesto'),
    ('confirm', 'Confirmado'),
    ('paid', 'Pagado')
]
STATE_PAGO_SELECTION = [
    ('pending', 'Pendiente'),
    ('today', 'Hoy'),
    ('overdue', 'Vencido')
]


class ComprobantePagoCliente(models.Model):
    _name = 'bicicletastore.comprobantepago.cliente'
    _description = 'Comprobantes de pago de cliente'
    _order = 'id desc'

    name = fields.Char(string='Serie-Correlativo', default='/')
    fecha_emision = fields.Date(string='Fecha de Emisión', default=fields.Date.context_today)
    fecha_vencimiento = fields.Date(string='Fecha de Vencimiento')
    cliente_id = fields.Many2one(
        'bicicletastore.cliente',
        string='Cliente',
        required=True,
        readonly=True,
        states={'budget': [('readonly', False)]},
    )
    vendedor_id = fields.Many2one('bicicletastore.vendedor', string='Vendedor')
    tipo = fields.Selection([('factura', 'Factura'), ('boleta', 'Boleta')], string='Tipo comprobante')
    termino_pago = fields.Selection(TERMINO_PAGO_SELECTION, string='Plazo pago')
    termino_pago_id = fields.Many2one('termino.pago', string='Plazo pago')
    payment_term_id = fields.Many2one('account.payment.term', string='Términos de pago')
    moneda = fields.Selection([('pen', 'Soles'), ('usd', 'Dólares')], string='Moneda')
    total = fields.Float(string='Total')
    saldo = fields.Float(string='Saldo')

    state = fields.Selection(
        STATE_SELECTION,
        default='budget',
        string='Estado'
    )
    state_pago = fields.Selection(
        STATE_PAGO_SELECTION,
        default='pending',
        compute='_compute_state_pago',
        string='Estado Pago',
        store=True
    )

    line_ids = fields.One2many(
        'bicicletastore.comprobantepago.cliente.bicicleta',
        'comprobante_id',
        string='Bicicletas'
    )
    pago_ids = fields.One2many(
        'bicicletastore.comprobantepago.historico',
        'comprobante_id',
        string='Pagos'
    )

    # @api.depends('line_ids')
    # def _compute_total(self):
    #     suma_total = 0
    #     for line in self.line_ids:
    #         suma_total += line.total
    #     self.total = suma_total

    @api.onchange('line_ids')
    def _onchange_line_ids(self):
        suma_total = 0
        for line in self.line_ids:
            suma_total += line.total
        return {
            'value': {
                'total': suma_total,
                'saldo': suma_total
            }
        }

    @api.onchange('pago_ids')
    def _onchange_pago_ids(self):
        suma_pago_total = 0
        for pago in self.pago_ids:
            # if pago.state == 'confirm':
            suma_pago_total += pago.monto
        return {
            'value': {
                'saldo': self.total - suma_pago_total
            }
        }

    @api.onchange('termino_pago_id')
    def _onchange_termino_pago_id(self):
        if self.fecha_emision and self.termino_pago_id:
            fecha_cal = self.fecha_emision + relativedelta(days=self.termino_pago_id.dias,
                                                           months=self.termino_pago_id.meses,
                                                           years=self.termino_pago_id.anios)
            return {
                'value': {'fecha_vencimiento': fecha_cal}
            }

    @api.depends('fecha_vencimiento')
    def _compute_state_pago(self):
        today = fields.Date.context_today(self)
        if self.fecha_vencimiento:
            if self.fecha_vencimiento > today:
                self.state_pago = 'pending'
            elif self.fecha_vencimiento == today:
                self.state_pago = 'today'
            elif self.fecha_vencimiento < today:
                self.state_pago = 'overdue'

    def action_set_confirm(self):
        self.ensure_one()
        self.state = 'confirm'

    def action_set_payment(self):
        self.ensure_one()
        view_id = self.env.ref('bicicleta_store.bicicletastore_comprobantepago_historico_view_form_wizard').id
        return {
            'name': 'Registrar un pago',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'bicicletastore.comprobantepago.historico',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {
                'default_comprobante_id': self.id,
                'default_monto': self.saldo,
            }
        }

    @api.model
    def create(self, values):
        if values.get('name', '/') == '/':
            values['name'] = self.env['ir.sequence'].next_by_code('comprobantepago.cliente', sequence_date=None) or '/'
        return super(ComprobantePagoCliente, self).create(values)


class ComprobantePagoClienteProducto(models.Model):
    _name = 'bicicletastore.comprobantepago.cliente.bicicleta'
    _description = 'Venta de bicicletas'

    comprobante_id = fields.Many2one('bicicletastore.comprobantepago.cliente', string='Comprobante')
    bicicleta_id = fields.Many2one('bicicletastore.bicicleta', string='Bicicleta', required=True)
    detalle = fields.Text(string='Detalle')
    precio = fields.Float(string='Precio', required=True)
    qty = fields.Float(string='Cantidad', required=True)
    total = fields.Float(string='Total', required=True)

    @api.onchange('bicicleta_id')
    def _onchange_bicicleta_id(self):
        return {'value': {'precio': self.bicicleta_id.precio}}

    @api.onchange('precio', 'qty')
    def _onchange_precio_qty(self):
        return {'value': {'total': self.precio * self.qty}}


class ComprobantePagoHistorico(models.Model):
    _name = 'bicicletastore.comprobantepago.historico'
    _description = 'Comprobantes de pago de historico'

    comprobante_id = fields.Many2one(
        'bicicletastore.comprobantepago.cliente',
        string='Comprobante'
    )
    fecha_pago = fields.Date(
        default=fields.Date.context_today,
        string='Fecha'
    )
    monto = fields.Float(string='Monto')
    state = fields.Selection(
        [('pending', 'Pendiente'),('confirm', 'Confirmado')],
        default='pending',
        string='Estado'
    )
    user_id = fields.Many2one(
        'res.users',
        default=lambda self: self.env.user.id
    )

    @api.onchange('monto')
    def _onchange_monto(self):
        if self.monto > self.comprobante_id.saldo:
            return {
                'value': {'monto': 0.0},
                'warning': {
                    'title': 'Error',
                    'message': 'No puede pagar más que el Saldo.'
                }
            }

    def action_guardar(self):
        self.ensure_one()
        saldo_final = self.comprobante_id.saldo - self.monto
        vals = {'saldo': saldo_final}
        if saldo_final == 0:
            vals['state'] = 'paid'
        self.comprobante_id.write(vals)
        return True
