from odoo import api, fields, models


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    register_date = fields.Date(string="Register_date")