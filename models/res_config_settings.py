# -*- coding: utf-8 -*-

from odoo import models, fields


class GitlabConfig(models.TransientModel):
    _inherit = "res.config.settings"

    enable_gitlab_integration = fields.Boolean(
        string="Enable Gitlab Integration",
        config_parameter="gitlab_pipeline_trigger.enable_gitlab_integration",
    )
    gitlab_private_token = fields.Char(
        string="Gitlab Private Token",
        config_parameter="gitlab_pipeline_trigger.gitlab_private_token",
    )
    gitlab_url = fields.Char(
        string="Gitlab URL",
        config_parameter="gitlab_pipeline_trigger.gitlab_url",
    )
