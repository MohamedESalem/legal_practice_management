{
    'name': 'Legal Case Management',
    'version': '1.0',
    'summary': 'Transform Odoo Projects into Cases & Matters for law firms',
    'description': 'Customizes the Odoo Project app for legal case and matter management.',
    'author': 'Mohamed Essam',
    'website': 'https://essamsalem.com',
    'category': 'Project',
    'depends': ['project', 'crm', 'contacts', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_views.xml',
        'views/crm_client_fields_view.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
} 