from odoo import models, fields


class InsertData(models.Model):
    
    _inherit = 'product.template'

    catagory_id = fields.Many2one('catagory')
    part_no = fields.Char()

class Catagory(models.Model):
    _name = 'catagory'

    name = fields.Char(string="name")

