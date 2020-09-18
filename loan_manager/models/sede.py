from odoo import fields, models

class Sede(models.Model):
    _name = 'res.sede'
    _description = 'Sede: Lugar donde se trabaja'

    name = fields.Char(string='Nombre', required=True)
    user_ids = fields.Many2many(
        'res.users',
        'res_sede_res_users_rel',
        'sede_id', 'user_id',
        string='Sedes'
    )
