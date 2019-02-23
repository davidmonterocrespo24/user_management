# -*- coding: utf-8 -*-
{
    'name': "User Management",

    'summary': """
        User info, accounts, groups""",

    'description': """
        User management for college.
    """,

    'author': "DINF DevTeam",
    'website': "http://www.uo.edu.cu",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'auditlog'],

    # always loaded
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'views/usermanagement_wizard_pass.xml',
        'views/usermanagement_system_groups.xml',
        'views/usermanagement_view_usuario.xml',
        'views/usermanagement_view_grupo.xml',
        'views/usermanagement_view_servicio.xml',
        'views/usermanagement_view_dominio.xml',
        'views/usermanagement_del_service_user.xml',
        'views/usermanagement_menu.xml',
    ],

    'application': True,

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
