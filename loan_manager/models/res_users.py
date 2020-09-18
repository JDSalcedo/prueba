from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    sede_ids = fields.Many2many(
        'res.sede',
        'res_sede_res_users_rel',
        'user_id', 'sede_id',
        string='Sedes'
    )
