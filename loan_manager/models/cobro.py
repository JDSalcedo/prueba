from odoo import api, fields, models
from odoo.exceptions import UserError


class Cobros(models.Model):
    _name = 'loanmanager.cobros'
    _description = 'Tabla de cobros'

    name = fields.Char(string='Serie del cobro', default='/')
    nombre_cliente = fields.Char(string='Nombre del Cliente', compute='_compute_nombre_cliente')
    fecha = fields.Date(string='Fecha', default=fields.Date.context_today, readonly=True)
    importe = fields.Float(string='Importe', required=True)
    prestamo_id = fields.Many2one('loanmanager.prestamo', string='Prestamo')

    @api.depends('prestamo_id')
    def _compute_nombre_cliente(self):
        self.nombre_cliente = '{} {}'.format(self.prestamo_id.cliente_id.name, self.prestamo_id.cliente_id.apellido)

    @api.model
    def create(self, values):
        values['name'] = self.env['ir.sequence'].next_by_code('comprobantecobro.cliente', sequence_date=None) or '/'
        pres_id = self.env['loanmanager.prestamo'].browse([values.get('prestamo_id')])
        if values.get('importe') > pres_id.saldo:
            raise UserError('No puede pagar más que el saldo')
        pres_id.saldo = pres_id.saldo - values.get('importe')
        if pres_id.saldo == 0:
            pres_id.estado = 'paid'
        return super(Cobros, self).create(values)

    def action_guardar(self):
        self.ensure_one()
        return True
