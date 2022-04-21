# -*- coding: utf-8 -*-

from email.policy import default
from odoo import api, fields, models
import calendar, datetime

class SaleOrderWizard(models.TransientModel):
    _name = 'sale.order.report.wizard'
    _description = 'Sale Order Report Wizard'

    date_start = fields.Date('Fecha Inicio', default=primer_dia_mes)
    date_end = fields.Date('Fecha Fin', default=ultimo_dia_mes)
    
    def primer_dia_mes(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month

        return datetime.date(year,month,1)

    def ultimo_dia_mes(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        last_day = calendar.monthrange(year, month)[1] ## último día

        return datetime.date(year,month,last_day)

    def action_search_orders(self):
        form_data = self.read()[0]

        orders = self.env['sale.order'].search_read([
            ('create_date', '>=', form_data['date_start']),
            ('create_date', '<=', form_data['date_end'])
        ])

        data = {
            'form_data': form_data,
            'orders': orders
        }

        return self.env.ref('flash_custom_reports.action_report_sale_order').report_action(self, data=data)