from odoo import models, fields
from datetime import timedelta


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'
    _order = "name"

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'The tag name must be unique.')
    ]

    name = fields.Char(string='Name', required=True)
    description = fields.Text('Description')
    color = fields.Integer(string="Color")
