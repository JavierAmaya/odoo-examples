from odoo import fields, models, api
from odoo.exceptions import UserError

class reportCommissionWizard(models.TransientModel):
    _name = 'report.commission.wizard'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    state = fields.Selection([('draft','Draft'),('done','Done'),('cancel','Canceled')], string="State", default="done")
    physician_ids = fields.Many2many('res.users',string="Physicians")

    @api.multi
    def action_print_report(self):
        data = {'start_date': self.start_date,'end_date': self.end_date, 'physician_ids': self.physician_ids.mapped('partner_id').ids,'state':self.state}
        data['model'] = 'report.commission.wizard'
        data['form'] = self.read()[0]
        for field in data['form'].keys():
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        return self.env.ref('gn_commission_seat.action_commission_report_xls').report_action(self, data=data)