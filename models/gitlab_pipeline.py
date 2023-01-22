from odoo import models, fields, api
import gitlab


class GitlabPipeline(models.Model):
    _name = 'gitlab.pipeline'
    _description = 'Gitlab Pipelines'

    gitlab_runner_id = fields.Many2one('gitlab.pipeline.runner')
    job_ids = fields.One2many(
        'gitlab.job', 
        'pipeline_id', 
        string='Pipelines'
    )
    pipeline_external_id = fields.Char('External ID')

    @api.model
    def create_jobs(self, jobs):
        pass