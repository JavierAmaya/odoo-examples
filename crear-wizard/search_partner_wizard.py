from odoo import models, api, fields
from dateutil.relativedelta import relativedelta

class WzSearchPartner(models.TransientModel):

    _name = 'wz.search.partner'

    name = fields.Char(string='Hola')
    
    def event_wizard(self):
        for rec in self:
            print('evento wizard')