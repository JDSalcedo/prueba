from odoo import fields, models


class ComprobantePagoCliente(models.Model):
    _name = 'bicicletastore.comprobantepago.cliente'
    _description = 'Comprobantes de pago de cliente'

    name = fields.Char(string='Serie-Correlativo')
    fecha_emision = fields.Date(string='Fecha de Emisión')
    fecha_vencimiento = fields.Date(string='Fecha de Vencimiento')
    cliente_id = fields.Many2one('bicicletastore.cliente', string='Cliente')
    vendedor_id = fields.Many2one('bicicletastore.vendedor', string='Vendedor')
