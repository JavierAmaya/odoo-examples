# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime
import io
import base64

class commissionReportXlsx(models.AbstractModel):
    _name = 'report.gn_commission_seat.commission_report_xls.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        cont = 1
        company_name = self.env.user.company_id.name
        info = self.get_data(data.get('start_date'),data.get('end_date'),data.get('physician_ids'),data.get('state'))

        cont+=1
        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 15, 'align': 'center', 'right': False, 'left': False, 'bottom': False, 'top': False, 'bold': True})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True, 'font_color':'#ffffff','bg_color':'#088A08'})
        format22 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': False, 'left': False,'bottom': False, 'top': False, 'bold': False})
        format23 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': False, 'left': False,'bottom': False, 'top': False, 'bold': True})
        format24 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': False, 'left': False,'bottom': False, 'top': False, 'bold': False})
        format25 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True, 'font_color':'#ffffff','bg_color':'#088A08'})
        format26 = workbook.add_format({'font_size': 10, 'align': 'right', 'right': False, 'left': False,'bottom': False, 'top': False, 'bold': True})
        format27 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True, 'font_color':'#000000','bg_color':'#ffff00'})
        format28 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': False, 'left': False,'bottom': False, 'top': False, 'bold': True, 'bg_color':'#ffff00'})
        ########### NUMBER FORMAT #######################################
        format3 = workbook.add_format({'align':'right', 'left':False, 'right':False, 'bottom': False, 'top': False, 'font_size': 10,'num_format': '#,##0.00'})
        format4 = workbook.add_format({'align':'right', 'left':False, 'right':False, 'bottom': False, 'top': False, 'bold':True ,'font_size': 10,'num_format': '#,##0.00'})
        format5 = workbook.add_format({'align':'right', 'left':False, 'right':False, 'bottom': False, 'top': False, 'bold':True ,'font_size': 10,'num_format': '#,##0.00', 'bg_color':'#ffff00'})
        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        red_mark = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8,
                                        'bg_color': 'red'})
        justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12})
        font_size_8.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')


        for commi in info:
            pos = 8
            num = 1
            sheet = workbook.add_worksheet(commi.get('physician'))
            sheet.set_column(0, 0, 5)
            sheet.set_column(1, 1, 15)
            sheet.set_column(2, 2, 35)
            sheet.set_column(3, 3, 20)
            sheet.set_column(4, 4, 30)
            sheet.set_column(5, 5, 18)
            sheet.set_column(6, 6, 15)
            sheet.set_column(7, 7, 15)
            sheet.set_column(8, 8, 15)
            sheet.set_column(9, 9, 15)
            sheet.set_column(10, 10, 15)
            sheet.set_column(11, 11, 15)
            sheet.set_column(12, 12, 15)
            sheet.set_column(13, 13, 15)
            sheet.set_column(14, 14, 15)
            sheet.set_column(15, 15, 15)
            sheet.set_column(16, 16, 15)

            sheet.merge_range('A3:N3', company_name, format11)
            sheet.merge_range('A4:N4', _('COMMISSION REPORT'), format11)

            sheet.merge_range('B6:C6', _('Start Date: %s')%(data.get('start_date')), format23)
            sheet.merge_range('D6:E6', _('End Date: %s')%(data.get('end_date')), format23)

            total = 0
            total_red_12_5 = 0
            total_red_1 = 0
            total_comision = 0
            total_net_total = 0
            total_gross = 0
            total_discount = 0
            total_comision_on = 0
            sheet.merge_range( 'A'+str(pos)+ ':' + 'D'+str(pos), _('Physician: %s')%(commi.get('physician')), format23)
            if commi['data'][0]['expired_payments']:
                sheet.merge_range( 'E'+str(pos)+ ':' + 'G'+str(pos), _('Payment on account: %s')%_('VENCIDO'), format28)
            else:
                sheet.merge_range( 'E'+str(pos)+ ':' + 'G'+str(pos), _('Payment on account: %s')%(commi.get('pac')), format28)
            sheet.write(pos, 0, _('No.'), format21)
            sheet.write(pos, 1, _('Date'), format21)
            sheet.write(pos, 2, _('Patient'), format21)
            sheet.write(pos, 3, _('Invoice'), format21)
            sheet.write(pos, 4, _('Insurance'), format21)
            sheet.write(pos, 5, _('Last Payment Date'), format21)
            sheet.write(pos, 6, _('Invoice State'), format21)
            if data.get('state') == 'done':
                sheet.write(pos, 7, _('Payment numbers'), format21)
                sheet.write(pos, 8, _('Gross Commission'), format21)
                sheet.write(pos, 9, _('Discount'), format21)
                sheet.write(pos, 10, _('Commission On'), format21)
                sheet.write(pos, 11, _('Commission (%)'), format21)
                sheet.write(pos, 12, _('Commission Amount'), format21)
                sheet.write(pos, 13, _('RED 12.5%'), format27)
                sheet.write(pos, 14, _('RED 1%'), format27)
                sheet.write(pos, 15, _('Commission 1%'), format27)
                sheet.write(pos, 16, _('Net Total'), format27)
            else:
                sheet.write(pos, 7, _('Gross Commission'), format21)
                sheet.write(pos, 8, _('Discount'), format21)
                sheet.write(pos, 9, _('Commission On'), format21)
                sheet.write(pos, 10, _('Commission (%)'), format21)
                sheet.write(pos, 11, _('Commission Amount'), format21)
                sheet.write(pos, 12, _('RED 12.5%'), format27)
                sheet.write(pos, 13, _('RED 1%'), format27)
                sheet.write(pos, 14, _('Commission 1%'), format27)
                sheet.write(pos, 15, _('Net Total'), format27)
            pos+=1
            for line in commi.get('data'):
                sheet.write(pos, 0, num, format25)    
                sheet.write(pos, 1, line.get('date'), format22)
                sheet.write(pos, 2, line.get('patient') or '', format22)
                sheet.write(pos, 3, line.get('invoice') or '', format22)
                sheet.write(pos, 4, line.get('insurance') or '', format22)
                sheet.write(pos, 5, line.get('last_payment_date') or '', format22)
                sheet.write(pos, 6, line.get('invoice_state') or '', format22)

                if data.get('state') == 'done':
                    sheet.write(pos, 7, line.get('number_payments') or '', format22)
                    sheet.write_number(pos, 8, line.get('gross_commission') or 0, format3)
                    sheet.write_number(pos, 9, line.get('discount') or 0, format3)
                    sheet.write_number(pos, 10, line.get('commission_on') or 0, format3)
                    sheet.write(pos, 11, line.get('commission_percentage') or '', format24)
                    sheet.write_number(pos, 12, line.get('commission_amount') or 0, format3)
                    sheet.write_number(pos, 13, line.get('red_12_5') or 0, format3)
                    sheet.write_number(pos, 14, line.get('red_1') or 0, format3)
                    sheet.write_number(pos, 15, line.get('comision_1') or 0, format3)
                    sheet.write_number(pos, 16, line.get('net_total') or 0, format3)
                else:
                    sheet.write_number(pos, 7, line.get('gross_commission') or 0, format3)
                    sheet.write_number(pos, 8, line.get('discount') or 0, format3)
                    sheet.write_number(pos, 9, line.get('commission_on') or 0, format3)
                    sheet.write(pos, 10, line.get('commission_percentage') or '', format24)
                    sheet.write_number(pos, 11, line.get('commission_amount') or 0, format3)
                    sheet.write_number(pos, 12, line.get('red_12_5') or 0, format3)
                    sheet.write_number(pos, 13, line.get('red_1') or 0, format3)
                    sheet.write_number(pos, 14, line.get('comision_1') or 0, format3)
                    sheet.write_number(pos, 15, line.get('net_total') or 0, format3)
                total += line.get('commission_amount')
                total_red_12_5 += line.get('red_12_5')
                total_red_1 += line.get('red_1')
                total_comision += line.get('comision_1')
                total_net_total += line.get('net_total')
                total_gross += line.get('gross_commission')
                total_discount += line.get('discount')
                total_comision_on += line.get('commission_on')
                pos+=1
                num+=1
            if data.get('state') == 'done':
                sheet.write(pos, 7, ("TOTAL:"), format26)
                sheet.write_number(pos, 8, total_gross or 0, format4)
                sheet.write_number(pos, 9, total_discount or 0, format4)
                sheet.write_number(pos, 10, total_comision_on or 0, format4)
                sheet.write_number(pos, 12, total or 0, format4)
                sheet.write_number(pos, 13, total_red_12_5 or 0, format5)
                sheet.write_number(pos, 14, total_red_1 or 0, format5)
                sheet.write_number(pos, 15, total_comision or 0, format5)
                sheet.write_number(pos, 16, total_net_total or 0, format5)
            else:
                sheet.write(pos, 6, ("TOTAL:"), format26)
                sheet.write_number(pos, 7, total_gross or 0, format4)
                sheet.write_number(pos, 8, total_discount or 0, format4)
                sheet.write_number(pos, 9, total_comision_on or 0, format4)
                sheet.write_number(pos, 11, total or 0, format4)
                sheet.write_number(pos, 12, total_red_12_5 or 0, format5)
                sheet.write_number(pos, 13, total_red_1 or 0, format5)
                sheet.write_number(pos, 14, total_comision or 0, format5)
                sheet.write_number(pos, 15, total_net_total or 0, format5)
            num = 1
            total = 0
            pos+=3

    def get_data(self, start_date, end_date, physician_ids, state):
        if physician_ids:
            commission_ids = self.env['acs.hms.commission'].search([('create_date','>=',start_date),('create_date','<=',end_date),('partner_id','in',physician_ids),('state','=',state)])
        else:
            commission_ids = self.env['acs.hms.commission'].search([('create_date','>=',start_date),('create_date','<=',end_date),('state','=',state)])

        physicians = []
        info = []
        expired_payments=False
        for comm in commission_ids:
            if comm.partner_id.payment_due_date:
                expired_payments = (datetime.strptime(comm.partner_id.payment_due_date,'%Y-%m-%d')<datetime.strptime(end_date,'%Y-%m-%d'))
            invoice_state = ''
            red_12_5 = 0
            red_1 = 0
            comision_1 = 0
            net_total = 0
            pac = _('YES')
            number_payments = ''
            if comm.invoice_status == 'paid':
                if comm.invoice_status == 'open':
                    invoice_state = _('Open')
                elif comm.invoice_status == 'paid':
                    invoice_state = _('Paid')

                percentage = str(comm.commission_percentage) + '%'
                if comm.commission_invoice_id.payment_ids:
                    number_payments = ', '.join(map(lambda x: x.name, comm.commission_invoice_id.payment_ids))
                
                if not comm.partner_id.payments_on_account or expired_payments:
                    red_12_5 = comm.commission_amount * 0.125
                    red_1 = comm.commission_amount * 0.01
                    pac = _('NO')
                
                if comm.commission_percentage == 100:
                    comision_1 = comm.commission_amount * 0.01

                net_total = comm.commission_amount - red_12_5 - red_1 - comision_1
                discount = 0
                if (comm.invoice_line_id.line_discount_amount):
                    discount = comm.invoice_line_id.line_discount_amount
                elif (comm.invoice_line_id.line_global_discount):
                    discount = comm.invoice_line_id.line_global_discount

                val = {
                    'date': self.change_format(comm.create_date),
                    'patient': comm.invoice_id.patient_id.name,
                    'commission_on': comm.commission_on,
                    'commission_percentage': percentage,
                    'commission_amount': comm.commission_amount,
                    'invoice': comm.invoice_id.move_name or comm.invoice_id.number,
                    'invoice_state': invoice_state,
                    'gross_commission': comm.invoice_line_id.price_unit,
                    'discount': discount,
                    'red_12_5': red_12_5,
                    'red_1': red_1,
                    'comision_1': comision_1,
                    'net_total': net_total,
                    'insurance': comm.invoice_id.insurance_company_id.name or _('N/A'),
                    'last_payment_date': self.get_last_payment(comm.invoice_id),
                    'number_payments': number_payments,
                    'expired_payments' : expired_payments 

                }
                if comm.partner_id.id in physicians:
                    info[physicians.index(comm.partner_id.id)]['data'].append(val)
                else:
                    physicians.append(comm.partner_id.id)
                    
                    info.append({
                        'physician': comm.partner_id.name,
                        'data': [val],
                        'pac': pac,
                        'expired_payments' : expired_payments 
                    })

        return info

    def get_last_payment(self, invoice):
        date = ''
        for payments in invoice._get_payments_vals():
            date = payments.get('date')
            break
        return self.change_format2(date)

    def change_format(self,date):
        if date:
            return datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')

    def change_format2(self,date):
        if date:
            return datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')