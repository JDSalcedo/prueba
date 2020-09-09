from odoo import fields, models

class TerminoPago(models.Model):
    _name = 'termino.pago'
    _description = 'Terminos de pago'

    name = fields.Char(string='Nombre', required=True)
    dias = fields.Integer(string='Días', required=True)
    meses = fields.Integer(string='Meses', required=True)
    anios = fields.Integer(string='Años', required=True)