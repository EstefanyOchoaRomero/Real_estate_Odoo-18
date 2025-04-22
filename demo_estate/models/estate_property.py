from odoo import models, fields
from datetime import timedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    
    
    name = fields.Char('Property Name', required=True)
    price = fields.Float(string="Price")
    partner_id = fields.Many2one('res.partner', string="Customer")


    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(
        string='Available From',
        default=lambda self: fields.Date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(string='Expected Price', required=True, copy=False)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Number of Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )
    active = fields.Boolean(string='Active', default=True)

    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], string="State", default='new', required=True, copy=False)

    status = fields.Selection([
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('pending', 'Pending')
    ], string="Status")
