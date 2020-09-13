from odoo import fields, models


class HrEmployeePrivate(models.Model):
    _inherit = 'hr.employee'

    tipo_trabajo = fields.Char(string='Tipo del Trabajo')
    nivel = fields.Char(string='Nivel')
    infracciones_ids = fields.One2many('hrprueba.infracciones', 'empleado_id', string="Infracciones")

    def action_set_infracciones(self):
        self.ensure_one()
        view_id = self.env.ref('hr_prueba.hrprueba_infracciones_view_form_wizard').id
        return{
            'name': 'Registrar Infraccion',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hrprueba.infracciones',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {
                'default_empleado_id': self.id
            }
        }
