from odoo import fields, models


class Cliente(models.Model):
    _name = 'loanmanager.cliente'
    _description = 'Tabla de clientes'

    name = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido')
    telefono = fields.Char(string='Teléfono')
    direccion = fields.Char(string='Dirección')
