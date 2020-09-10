from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    direccion_entrega = fields.Char(string='Dirección de entrega')
    recordatorio_date = fields.Date(string='Fecha de recordatorio')
