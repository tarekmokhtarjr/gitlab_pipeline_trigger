from odoo import models, fields, api
import gitlab


class GitlabJob(models.Model):
    _name = 'gitlab.job'
    _description = 'Gitlab Jobs'

    pipeline_id = fields.Many2one('gitlab.pipeline')
    job_external_id = fields.Char('External ID')
