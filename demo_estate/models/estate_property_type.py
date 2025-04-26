from odoo import models, fields
from datetime import timedelta


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'
    _order = "name"
    

    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'The name of the property type must be unique.')
    ]

    name = fields.Char(required=True)
    code = fields.Char('Code')
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer("Sequence", default=10)
