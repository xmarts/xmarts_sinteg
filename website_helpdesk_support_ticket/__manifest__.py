# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Helpdesk Support Ticket and Issue Management',
    'price': 59.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'summary': """This module allow you manage your customer support ticket, ticket portal, billings for support, Timesheets.""",
    'description': """
Website Helpdesk Support Ticket
helpdesk
helpdesk support
customer helpdesk
customer Helpdesk support
Helpdesk support request
Helpdesk support ticket
ticket
Helpdesk customer query
Helpdesk customer help
Customer Maintaince request
Customer service request
Website Helpdesk ticket
website request customer
This module add website helpdesk support ticket.
Website Helpdesk Support Ticket
helpdesk
help desk
helpdesk support system
website_support
crm_helpdesk
Helpdesk Management
unique ticket number to customer automatically
being able to reply to incoming emails to communicate with customer
seeing all a customer's incoming help desk requests in context against customer object
unique ticket number per issue
print Helpdesk Ticket

Attachment on website Helpdesk Support
Message on website Helpdesk Support
Add attchment
Add message
Send Message Helpdesk Support
Attachment add Helpdesk Support
Multiple attachments Helpdesk Support
Add multiple attachments Helpdesk Support
Add attachments on website
App to manage your customer tickets and requests
                Website Support Ticket:
                    - Support Detail
Tags:
customer support
support request
support ticket
ticket
customer query
customer help
customer maintaince request
customer service request
website support ticket
website request customer

helpdesk
help desk
helpdesk support system
website_support
crm_helpdesk
Helpdesk Management
unique ticket number to customer automatically
being able to reply to incoming emails to communicate with customer
seeing all a customer's incoming help desk requests in context against customer object
unique ticket number per issue
                Website Support Ticket Invoice:

probuse
mustufa rangwala
mustufa
customer support Invoice
support request Invoice
support ticket Invoice
ticket Invoice
customer query 
customer help
customer maintaince request Invoice
customer service request Invoice
website support ticket Invoice
website request customer Invoice
ticket invoice 
customer invoice for support tickets

               Website Support Ticket My Account:
Customer Portal (My Account) - Support Tickets

Tags:
customer support Portal
support request Portal
support ticket Portal
ticket Portal
customer query 
customer help
customer maintaince request Portal
customer service request Portal
website support ticket Portal
website request customer Portal
ticket Portal 
customer Portal for support tickets

helpdesk
help desk
helpdesk support system
website_support
crm_helpdesk
Helpdesk Management
unique ticket number to customer automatically
being able to reply to incoming emails to communicate with customer
seeing all a customer's incoming help desk requests in context against customer object
unique ticket number per issue

                Website Support Ticket Timesheet:
Customer Portal (Timesheett) - Support Tickets

customer support
support request
support ticket
ticket
customer query
customer help
customer maintaince request
customer service request
website support ticket
website request customer
support timesheet
support time
support hr timesheet
employee timesheet
Website Helpdesk Support Ticket

This module allow you manage your customer support ticket, ticket portal, billings for support, Timesheets.

Main Features
* Your Customer can send support ticket/helpdesk request from your website.
* Generation of unique ticket on submission and record it as ticket in backend.
* Customer can check status of all support tickets submitted by him/her on My Account page.
* Print PDF - Helpdesk Support Ticket
* Support User / Technician can communitcate with customer using chatter and fill timesheet.
* Support Manager can close ticket and send bill to customer.
* Customer can give feedback and rating of ticket.
Menus Available:
time in
time out
sign in
sign out
billable
customer bill
Helpdesk
Helpdesk/Configuration
Helpdesk/Configuration/Helpdesk Teams
Helpdesk/Helpdesk
Helpdesk/Helpdesk/Helpdesk Tickets
Helpdesk/Reports
Helpdesk/Reports/Helpdesk Analysis
Helpdesk Users

Customer ===> William Hills
Support Manager ==> Peter Pinaker
Support User ==> Martin Luther

prepaid support hours
prepaid
prepaid support
prepaid customer
prepaid invoice



This module allow Manager to create Timesheets invoice.
Timesheets to Invoice
Create Timesheets invoice
Timesheet Customer Invoice Create
timesheet invoice
customer invoice timesheet
billable
bill to customer
customer bill
support hours timesheet invoice
timesheet by project
helpdesk 
helpdesk invoice
customer invoice on employee timesheet
Timesheet Invoice Create
This module allow you to create invoice from employee timesheets.
timesheet bill
customer timesheet
invoice timesheet
timesheet report to customer
timesheet activities
my timesheet
invoice bill
invoice from timesheet
analytic line
anlaytic
employee timesheet details
invoice based on timesheet
invoice from timesheet
invoice on timesheet
timesheet on invoice
Customer Invoices from Timesheets
This module allow you to create invoice from employee timesheets.
Allow you to create customer invoice from list of timesheets. Customer invoices will be created based on group by Project and Customer.
You can configure rate on customer form which will be passed to related projects of that customer and then related task of customer project.
Menus Available:
Invoicing
Configure Rate on Customer Form

Timesheet Lines to Create Customer Invoices

In list of timesheet system will display only billable timesheet lines which have not been invoiced yet.

Select timesheet lines for which you want to create customer invoice.

Click on Make Invoice wizard action to create customer invoice
Click Create Invoice Button on Wizard

Created Invoices after Running Wizard

This module allows Timesheet Manager to print Timesheet Report.
Timesheet Employee Weekly Report
print Timesheet PDF Report
Timesheet Report PDF
Timesheet QWEB Report
This module allows Timesheet Manager to print Weekly Timesheet Report.
week timesheet
weekly timesheet
employee timesheet
employee week timesheet
employee weekly timesheet
timesheet pdf report
timesheet report
customer timesheet report
customer timesheet
timesheet employee pdf
employee print timesheet
print odoo timesheet
probuse
timesheet
timesheet pdf report
weekly
week
timesheet week
analytic line
hr timesheet sheet
timesheet by project
timesheet line by project
timesheet line on project
project on timesheet
timesheet sheet
timesheet sheet employee
timesheet report to customer
timesheet activities
my timesheet
​project issue
issue project
project helpdesk
project case
project claim
claim order
project issue management
issue project management
project issuer
customer issue
customer feedback
customer case
customer project issue
odoo 11 project issue
project issue 11 odoo
project issue odoo 11
project task
support
project support
support manager
issue manager
issue operator​




    """,
    'author': "Probuse Consulting Service Pvt. Ltd.",
    'website': "http://www.probuse.com",
    'support': 'contact@probuse.com',
    'images': ['static/description/img1.jpeg'],
     'live_test_url': 'https://youtu.be/yaf1p2zsQzM',
    'version': '2.9.1',
    'category' : 'Project',
    'depends': [
                #'hr_timesheet_sheet',
                'sale_management',
                'hr_timesheet',
                'project',
#                 'website_portal',
                'portal',
                'sales_team',
                'crm',
                'account',
                'website',
                ],
    'data':[
        'report/support_request.xml',
        'datas/helpdesk_support_sequence.xml',
        'datas/mail_template_ticket.xml',
        'datas/helpdesk_team_data.xml',
        'datas/helpdesk_stages_data.xml',
        'security/helpdesk_security.xml',
        'security/ir.model.access.csv',
        'views/website_mail_message_template.xml',
        'views/helpdesk_stages_views.xml',
        'views/helpdesk_support_view.xml',
        'views/ticket_type_view.xml',
        'views/type_of_subject_view.xml',
        'views/helpdesk_support_template.xml',
        'views/hr_timesheet_sheet_view.xml',
        'views/support_team_view.xml',
        'views/my_ticket.xml',
#  odoo12      'views/ticket_attachment.xml',
        'views/successfull.xml',
        'views/task.xml',
        'views/feedback.xml',
        'views/thankyou.xml',
#  odoo12      'report/helpdesk_analysis.xml',
        'views/analytic_account_view.xml',
        'views/res_partner_form_view.xml',
        'views/project_form_view.xml',
        'views/project_task_form_view.xml',
#  odoo12      'views/helpdesk_invoice_view.xml',
#         'report/weekly_time_sheet_report_view.xml',
#         'wizard/weekly_timesheet_report.xml',
#  odoo12      'wizard/task_timesheet_invoice.xml',
        'views/report_analysis.xml',
    ],
    'installable' : True,
    'application' : False,
    #'auto_install' : True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
