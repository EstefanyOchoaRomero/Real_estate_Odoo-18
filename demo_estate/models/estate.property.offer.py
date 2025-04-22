from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float('Price')
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], 'Status')
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")



# property_id = fields.Many2one('estate.property', 'Property', required=True)