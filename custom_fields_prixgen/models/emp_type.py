from odoo import api, fields, models, _

class Employee(models.Model):
    _inherit = "hr.employee"

    employee_type = fields.Selection([
        ('employee', 'True'),
        ('consultant', 'False'),
    ],string='Employee')
    emp_type = fields.Boolean('If Employee')
