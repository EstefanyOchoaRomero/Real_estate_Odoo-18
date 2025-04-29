from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price > 0)', 'Selling price must be positive.')
    ]

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
                raise UserError("Cancelled properties cannot be marked as sold.")
            record.state = 'sold'
            record.status = 'sold'

        self.create_invoice()

    def action_mark_as_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            record.state = 'cancelled'
            record.status = 'cancelled'   

    @api.constrains('selling_price', 'expected_price')
    def _check_minimum_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            minimum_accepted_price = record.expected_price * 0.9
            if float_compare(record.selling_price, minimum_accepted_price, precision_digits=2) < 0:
                raise ValidationError(
                    f"The selling price ({record.selling_price}) cannot be lower than 90% of the expected price ({minimum_accepted_price})."
                )

    def _compute_show_buttons(self):
        for rec in self:
            rec.show_action_buttons = rec.state not in ('sold', 'canceled')

    @api.depends('garden')
    def _compute_show_garden_fields(self):
        for record in self:
            record.show_garden_fields = record.garden

    def unlink(self):
        for property in self:
            if property.state not in ['new', 'cancelled']:
                raise UserError("You cannot delete a property unless it is in 'New' or 'Cancelled' state.")
        return super(EstateProperty, self).unlink()

    @api.ondelete(at_uninstall=False)
    def _check_deletable_state(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError("You can only delete properties in 'New' or 'Cancelled' state.")

    show_garden_fields = fields.Boolean(compute="_compute_show_garden_fields")
    show_action_buttons = fields.Boolean(compute="_compute_show_buttons")
    property_id = fields.Many2one('estate.property.offer', string="Property Offer")
    best_price = fields.Float(string="Best Price", compute='compute_best_price')
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
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
    name_title = fields.Char(string='Title')
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
    total_area = fields.Float(compute="compute_total_area")
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
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled')], string="Status")

    def create_invoice(self):

        for property in self:
            if not property.buyer_id:
                raise UserError("Buyer is missing.")

            if not property.best_price:
                raise UserError("Price is missing.")

            journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
            if not journal:
                raise UserError("No sales journal found.")
            commission_fee = property.best_price * 0.06
            admin_fee = 100.00
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': property.buyer_id.id,
                'invoice_date': fields.Date.today(),
                'journal_id': journal.id,
                'invoice_line_ids': [(0, 0, {
                    'name': property.name,
                    'quantity': 1,
                    'price_unit': property.best_price,
                }), (0, 0, {
                    'name': 'Commission (6%)',
                    'quantity': 1,
                    'price_unit': commission_fee,
                }), (0, 0, {
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': admin_fee,
                })],

            })

            invoice.action_post()
