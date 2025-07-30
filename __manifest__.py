{
    'name': 'Legal Case Management',
    'version': '1.0',
    'summary': 'Transform Odoo Projects into Cases & Matters for law firms',
    'description': 'Customizes the Odoo Project app for legal case and matter management.',
    'author': 'Mohamed Essam',
    'website': 'https://essamsalem.com',
    'category': 'Project',
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
} 