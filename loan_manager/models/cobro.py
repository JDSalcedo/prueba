from odoo import fields, models


class Cobros(models.Model):
    _name = 'loanmanager.cobros'
    _description = 'Tabla de cobros'

    name = fields.Char(string='Serie del cobro', default='/')
    fecha = fields.Date(string='Fecha', default=fields.Date.context_today)
    importe = fields.Float(string='Importe')
    prestamo_id = fields.Many2one('loanmanager.prestamo', string='Prestamo')

    def action_guardar(self):
        self.ensure_one()
        self.name = self.env['ir.sequence'].next_by_code('comprobantecobro.cliente', sequence_date=None) or '/'
        saldo_final = self.prestamo_id.saldo - self.importe
        valores = {'saldo':saldo_final}
        if saldo_final == 0:
            valores['prestamo_id.estado'] = 'paid'
        self.prestamo_id.write(valores)
        return True