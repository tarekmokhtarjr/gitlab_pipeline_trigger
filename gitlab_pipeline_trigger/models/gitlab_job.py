from odoo import models, fields, _
import gitlab


class GitlabJob(models.Model):
    _name = "gitlab.job"
    _description = "Gitlab Jobs"
    _rec_name = "job_external_id"

    name = fields.Char("name")
    job_external_id = fields.Char("External ID")
    pipeline_id = fields.Many2one("gitlab.pipeline")
    web_url = fields.Char(string="Job URL")
