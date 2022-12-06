# -*- coding: utf-8 -*-

from odoo import models, fields, api


class GitlabConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_gitlab_integration = fields.Boolean(string="Enable Gitlab Integration")
    gitlab_private_token = fields.Char(string="Gitlab Private Token")
    gitlab_url = fields.Char(string="Gitlab URL")