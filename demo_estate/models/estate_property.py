from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    @api.depends('living_area','garden_area') 
    def compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def compute_best_price(self):
        for record in self:
            offers = record.offer_ids.mapped('price')
            record.best_price = max(offers) if offers else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_mark_as_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Canceled properties cannot be marked as sold.")
            record.state = 'sold'

    def action_mark_as_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            record.state = 'cancelled'


    property_id = fields.Many2one('estate.property.offer', string="Property Offer")
    best_price = fields.Float(string="Best Price", compute='compute_best_price')
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
    total_area = fields.Float(compute="compute_total_area")
    offer_ids = fields.One2many(
        "estate.property.offer", 'property_id', string="Property Offers")
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    salesperson_id = fields.Many2one(
        'res.users', string="Salesperson",
        default=lambda self: self.env.user.id)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    name = fields.Char('Property Name', required=True)
    price = fields.Float(string="Price")
    partner_id = fields.Many2one('res.partner', string="Customer")
    name_title = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(
        string='Available From',
        default=lambda self:
        fields.Date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(
        string='Expected Price', required=True, copy=False)
    selling_price = fields.Float(
        string='Selling Price', readonly=True, copy=False)
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
    