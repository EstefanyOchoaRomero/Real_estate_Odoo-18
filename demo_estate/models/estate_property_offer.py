from odoo import models, fields, api
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float('Price')

    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='Status', copy=False)

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True
    )

    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True
    )

    validity = fields.Integer(
        string="Validity (days)", default=7)

    date_deadline = fields.Date(
        string="Date Deadline", 
        compute="compute_date_deadline", 
        inverse="inverse_date_deadline")

    @api.depends('create_date', 'validity')
    def compute_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = fields.Datetime.from_string(record.create_date).date()
                record.date_deadline = create_date + timedelta(days=record.validity)
                
    def inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date).days
                