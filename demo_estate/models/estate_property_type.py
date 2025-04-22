from odoo import models, fields
from datetime import timedelta


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'

    name = fields.Char(required=True)
    code = fields.Char('Code')