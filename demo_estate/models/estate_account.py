from odoo import models, fields
from odoo.exceptions import UserError


class EstateAccount(models.Model):
    _inherit = 'estate.property'

    # def action_sold(self):
    #     print("✅ Entrando a action_sold")

    #     # Llamar al original
    #     res = super().action_sold()

    #     for property in self:
    #         if not property.buyer_id:
    #             raise UserError("Buyer is missing.")

    #         if not property.price:
    #             raise UserError("Price is missing.")

    #         journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
    #         if not journal:
    #             raise UserError("No sales journal found.")

    #         invoice = self.env['account.move'].create({
    #             'move_type': 'out_invoice',
    #             'partner_id': property.buyer_id.id,
    #             'invoice_date': fields.Date.today(),
    #             'journal_id': journal.id,
    #             'line_ids': [(0, 0, {
    #                 'name': property.name,
    #                 'quantity': 1,
    #                 'price_unit': property.price,
    #             })],
    #         })

    #         invoice.action_post()
    #         print(f"✅ Invoice created for: {property.name}")

    #     return res





