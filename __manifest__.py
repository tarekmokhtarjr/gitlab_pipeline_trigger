# -*- coding: utf-8 -*-
{
    'name': "Gitlab Integration",

    'summary': """
        A module to integrate Odoo with Gitlab to run pipelines for projects""",

    'description': """
        A module to integrate Odoo with Gitlab to run pipelines for projects
    """,

    'author': "Ahmed Mokhtar",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'base_setup',
        'project'
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
    ],

    'external_dependencies': {
        'python': ['python-gitlab'],
    },
}
