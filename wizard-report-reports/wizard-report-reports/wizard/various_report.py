from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class variousReportWizard(models.TransientModel):
    _name = 'various.report.wizard'

    @api.model
    def get_actual_year(self):
        return datetime.now().year

    report_type = fields.Selection([('medical_fees','Medical Fees'),('general_consultations','General Consultations'),
                                    ('advances_not_applied','Advances not Applied'),('detailed_account_insurer','Detailed account Statement by Insurer'),
                                    ('cust_acc_statement', 'Customer Account Statement'),('summary_account_insurer', 'Summary account Statement by Insurer'),
                                    ('cxc_insurance','Accounts Receivable Insurance'),('det_med_ma_pro','Detailed Medical Management and Procedures'),
                                    ('summ_med_ma_pro','Summary Medical Management and Procedures'),('clinic_rental', 'Clinic Rental'),
                                    ('age_of_detailed','Age of Detailed Insurance Balances'),('age_of_summary','Age of Summary Insurance Balances'),
                                    ('sale_report','Sale Report'),('pre_req_sur','Prescriptions, Requisition and Surgeries'),
                                    ('laboratory_report','Laboratory Report'),('account_control','Account Control'),('surgeries_report','Surgeries')], default="medical_fees")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    physician_ids = fields.Many2many('hms.physician',string="Physicians")

    ################### General Consultations  #####################################
    year = fields.Integer('Year', default=get_actual_year)
    initial_month = fields.Selection([('1','January'),('2','February'),('3','March'),('4','April'),('5','May'),
                                    ('6','June'),('7','July'),('8','August'),('9','September'),('10','October'),
                                    ('11','November'),('12','December')],default="1" , string="Initial Month")
    final_month = fields.Selection([('1','January'),('2','February'),('3','March'),('4','April'),('5','May'),
                                    ('6','June'),('7','July'),('8','August'),('9','September'),('10','October'),
                                    ('11','November'),('12','December')],default="2",string="Final Month")
    appointment_state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirm'),
                                        ('waiting', 'Waiting'),('in_consultation', 'In consultation'),
                                        ('to_invoice', 'To Invoice'),('done', 'Done'),
                                        ('cancel', 'Cancelled')], string='State')

    ################### Detailed account Statement by Insurer  #####################################
    insurers_ids = fields.Many2many('hms.insurance.company',string="Insurers")

    @api.multi
    def action_print_report(self):
        vals = {
            'start_date': self.start_date,
            'end_date': self.end_date, 
            'physician_ids': self.physician_ids.mapped('partner_id').ids,
            'year': self.year,
            'initial_month': self.initial_month,
            'final_month': self.final_month,
            'appointment_state': self.appointment_state,
            'insurers_ids': self.insurers_ids.ids
        }
        data = vals
        data['model'] = 'various.report.wizard'
        data['form'] = self.read()[0]
        for field in data['form'].keys():
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        if self.report_type == 'medical_fees':
            return self.env.ref('gn_commission_seat.action_medical_fees_xls').report_action(self, data=data)
        if self.report_type == 'unbilled_charges':
            return self.env.ref('gn_commission_seat.action_medical_fees_xls').report_action(self, data=data)
        if self.report_type == 'general_consultations':
            return self.env.ref('gn_commission_seat.action_general_consultations_xls').report_action(self, data=data)
        if self.report_type == 'advances_not_applied':
            return self.env.ref('gn_commission_seat.action_advance_not_applied_xls').report_action(self, data=data)
        if self.report_type == 'detailed_account_insurer':
            return self.env.ref('gn_commission_seat.action_detailed_account_insurer_xls').report_action(self, data=data)
        if self.report_type == 'cust_acc_statement':
            return self.env.ref('gn_commission_seat.action_customer_account_statement_xls').report_action(self, data=data)
        if self.report_type == 'summary_account_insurer':
            return self.env.ref('gn_commission_seat.action_summary_account_insurer_xls').report_action(self, data=data)
        if self.report_type == 'cxc_insurance':
            return self.env.ref('gn_commission_seat.action_cxc_insurance_xls').report_action(self, data=data)
        if self.report_type == 'det_med_ma_pro':
            return self.env.ref('gn_commission_seat.action_det_med_ma_pro_xls').report_action(self, data=data)
        if self.report_type == 'summ_med_ma_pro':
            return self.env.ref('gn_commission_seat.action_summ_med_ma_pro_xls').report_action(self, data=data)
        if self.report_type == 'clinic_rental':
            return self.env.ref('gn_commission_seat.action_clinic_rental_xls').report_action(self, data=data)
        if self.report_type == 'age_of_detailed':
            return self.env.ref('gn_commission_seat.action_age_of_detailed_xls').report_action(self, data=data)
        if self.report_type == 'age_of_summary':
            return self.env.ref('gn_commission_seat.action_age_of_summary_xls').report_action(self, data=data)
        if self.report_type == 'sale_report':
            return self.env.ref('gn_commission_seat.action_sale_report_xls').report_action(self, data=data)
        if self.report_type == 'pre_req_sur':
            return self.env.ref('gn_commission_seat.action_pre_req_sur_xls').report_action(self, data=data)
        if self.report_type == 'laboratory_report':
            return self.env.ref('gn_commission_seat.action_laboratory_report_xls').report_action(self, data=data)
        if self.report_type == 'account_control':
            return self.env.ref('gn_commission_seat.action_account_control_xls').report_action(self, data=data)
        if self.report_type == 'surgeries_report':
            #print("==================data=======>",data)
            return self.env.ref('gn_commission_seat.action_surgeries_report_xls').report_action(self, data=data)

    @api.constrains('start_date','end_date')
    def validate_dates(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError(_('The initial date can not be greater than the final.'))

    @api.constrains('year')
    def validate_year(self):
        if self.report_type in ['general_consultations','summ_med_ma_pro']:
            if len(str(self.year)) < 4 or len(str(self.year)) > 4:
                raise ValidationError(_('The year must have 4 digits'))