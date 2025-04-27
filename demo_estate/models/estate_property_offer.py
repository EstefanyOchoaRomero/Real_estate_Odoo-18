from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'
    _order = "price desc"


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
    
    currency_id = fields.Many2one(
        'res.currency', 
        string='Currency', 
        default=lambda self: self.env.company.currency_id)
    
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', store=True)

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
            self.property_id._check_minimum_selling_price()

    def action_reject_offer(self):
        for offer in self:
            offer.status = 'refused'            

    @api.constrains('price', 'status')
    def _check_price_threshold_on_accept(self):
        for offer in self:
            if offer.status == 'accepted':
                expected = offer.property_id.expected_price
                threshold = expected * 0.9
                if float_compare(offer.price, threshold, precision_digits=2) < 0:
                    raise ValidationError("Accepted offers must be at least 90% of the expected price.")

    def action_accept_offer(self):
        for offer in self:
            expected = offer.property_id.expected_price
            threshold = expected * 0.9

            # Validar antes de aceptar
            if float_compare(offer.price, threshold, precision_rounding=offer.currency_id.rounding) < 0:
                raise ValidationError("Offer must be at least 90% of expected price.")

            # Cancelar otras ofertas
            other_offers = offer.property_id.offer_ids - offer
            other_offers.write({'status': 'refused'})

            # Aceptar la oferta
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id

    def action_refuse_offer(self):
        for offer in self:
            if offer.status == 'refused':
                raise UserError("This offer has already been refused.")
            offer.status = 'refused'
