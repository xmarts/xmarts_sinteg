# -*- coding: utf-8 -*-
{
    'name': "sinteg",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','rma_ept','contacts','purchase','website_helpdesk_support_ticket','xmarts_order_request','account'],

    # always loaded
    'data': [
        #'data/mail_template.xml',
        'reports/purchase_quotation_templates.xml',
        'reports/formato_ruta.xml',
        'reports/report_recibo_ticket.xml',
        'reports/report_recibo_ticket_dos.xml',
        'reports/reports_menu.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}