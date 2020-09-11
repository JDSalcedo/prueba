from odoo import fields, models


class HrEmployeePrivate(models.Model):
    _inherit = 'hr.employee'

    tipo_trabajo = fields.Char(string='Tipo del Trabajo')
    nivel = fields.Char(string='Nivel')


