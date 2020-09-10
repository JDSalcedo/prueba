from odoo import api, fields, models


STATE_SELECTION = [
    ('owe', 'debiendo'),
    ('paid', 'pagado')
]

class Prestamo(models.Model):
    _name = 'loanmanager.prestamo'
    _description = 'Tabla de préstamos'

    name = fields.Char(string='Serie Corelativo', default='/', readonly=True)
    monto_prestado = fields.Float(string='Monto Prestado')
    fecha = fields.Date(string='Fecha', default=fields.Date.context_today, readonly=True)
    cliente_id = fields.Many2one('loanmanager.cliente', string='Cliente')
    cobro_ids = fields.One2many('loanmanager.cobros', 'prestamo_id', string='Cobros')
    saldo = fields.Float(string="Saldo")
    estado = fields.Selection(STATE_SELECTION, string='Estado', default='owe')



    def action_set_cobro(self):
        self.ensure_one()
        view_id = self.env.ref('loan_manager.loanmanager_cobros_view_form_wizard').id
        return {
            'name': 'Registrar un cobro',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'loanmanager.cobros',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {
                'default_prestamo_id': self.id,
            }
        }

    @api.model
    def create(self, values):
        if values.get('name', '/') == '/':
            values['name'] = self.env['ir.sequence'].next_by_code('comprobanteprestamo.cliente', sequence_date=None) or '/'
        return super(Prestamo, self).create(values)

    @api.onchange('monto_prestado')
    def _onchange_monto_prestado(self):
        return{
            'value': {
                'saldo': self.monto_prestado
            }
        }

    @api.onchange('cobros_ids')
    def _onchange_cobros_ids(self):
        suma_cobros = 0
        for cobro in self.cobro_ids:
            suma_cobros += cobro.importe
        return {
            'values': {
                'saldo': self.monto_prestado - suma_cobros
            }
        }






