{
    'name': 'Legal Practice Management',
    'version': '1.0',
    'summary': 'Transform Odoo Projects, CRM and Contacts into Legal Practice Management for law firms, with suitable legal fields in CRM client profiles.',
    'description': 'Customizes the Odoo Project app for legal case and matter management, and adds suitable legal fields in the client\'s CRM profile.',
    'author': 'Mohamed Essam',
    'website': 'https://essamsalem.com',
    'category': 'Project',
    'depends': ['project', 'crm', 'contacts', 'base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/legal_case_data.xml',
        'views/project_views.xml',
        'views/crm_client_fields_view.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'images': [],
    'demo': [],
    'test': [],
    'css': [],
    'js': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 0,
    
    # Use post_init_hook to run code automatically *after* installation is complete.
    # Here we call a function that ensures 'sale_project' is uninstalled,
    # because that module introduces unwanted links between Sales and Projects
    # which conflict with the Legal Practice Management logic.
    'post_init_hook': 'post_init_hook'
}