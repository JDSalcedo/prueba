from odoo import api, fields, models


class Cobros(models.Model):
    _name = 'loanmanager.cobros'
    _description = 'Tabla de cobros'

    name = fields.Char(string='Serie del cobro', default='/')
    fecha = fields.Date(string='Fecha', default=fields.Date.context_today)
    importe = fields.Float(string='Importe')
    prestamo_id = fields.Many2one('loanmanager.prestamo', string='Prestamo')

    @api.onchange('importe')
    def _onchange_importe(self):
        if self.importe > self.prestamo_id.saldo:
            return{
                'value': {
                    'monto': 0.0
                },
                'warning': {
                    'title': 'Error',
                    'message': 'No puede pagar más que el saldo'
                }
            }

    def action_guardar(self):
        self.ensure_one()
        self.name = self.env['ir.sequence'].next_by_code('comprobantecobro.cliente', sequence_date=None) or '/'
        saldo_final = self.prestamo_id.saldo - self.importe
        valores = {'saldo': saldo_final}
        if saldo_final == 0:
            valores['estado'] = 'paid'
        self.prestamo_id.write(valores)
        return True
