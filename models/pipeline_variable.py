from odoo import models, fields, api
import gitlab


class PipelineVariable(models.Model):
    _name = 'pipeline.variable'
    _description = 'Pipeline Variables'

    key = fields.Char('Key')
    value = fields.Char('Value')
    value_hidden = fields.Char('Value', related='value')
    gitlab_runner_id = fields.Many2one('gitlab.pipeline.runner')
