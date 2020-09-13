from odoo import api, fields, models


class Infracciones(models.Model):
    _name = 'hrprueba.infracciones'

    name = fields.Char(string='Nombre de Infracción')
    fecha = fields.Date(string='Fecha', default=fields.Date.context_today, readonly=True)
    puntuacion = fields.Integer(string='Puntuacióm')
    descripcion = fields.Text(string='Descripción', required=True)
    empleado_id = fields.Many2one('hr.employee', string='Empleado')
