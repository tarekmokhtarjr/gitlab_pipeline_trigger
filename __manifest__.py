# -*- coding: utf-8 -*-
{
    "name": "Gitlab Pipeline Trigger",
    "summary": """
        A module to integrate Odoo with Gitlab to run pipelines for projects""",
    "description": """
        A module to integrate Odoo with Gitlab to run pipelines for projects
    """,
    "author": "Ahmed Mokhtar",
    "category": "Tools",
    "version": "15.0.1",
    "depends": ["base", "base_setup", "project"],
    "data": [
        "security/ir.model.access.csv",
        "views/gitlab_jobs_views.xml",
        "views/gitlab_pipeline_views.xml",
        "views/gitlab_pipeline_runner_views.xml",
        "views/project_project_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "external_dependencies": {
        "python": ["python-gitlab"],
    },
    "application": True,
}
