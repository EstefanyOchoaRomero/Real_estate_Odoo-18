from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError


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

    def action_approve_offer(self):
        for offer in self:
            offer.status = 'accepted'

    def action_reject_offer(self):
        for offer in self:
            offer.status = 'refused'            

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.status == 'sold':
                raise UserError("This property is already sold, you cannot accept new offers.")
            if offer.status == 'accepted':
                raise UserError("This offer has already been accepted.")
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.status = 'offer_accepted'

    def action_refuse_offer(self):
        for offer in self:
            if offer.status == 'refused':
                raise UserError("This offer has already been refused.")
            offer.status = 'refused'
