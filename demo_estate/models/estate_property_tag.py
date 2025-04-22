from odoo import models, fields
from datetime import timedelta


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'

    name = fields.Char(string='Name', required=True)
    description = fields.Text('Description')
