from odoo import models, fields, _
import gitlab


class GitlabPipeline(models.Model):
    _name = "gitlab.pipeline"
    _description = "Gitlab Pipelines"
    _rec_name = "pipeline_external_id"

    gitlab_runner_id = fields.Many2one("gitlab.pipeline.runner")
    job_ids = fields.One2many("gitlab.job", "pipeline_id", string="Pipelines")
    job_count = fields.Integer(compute="_compute_job_count", string="Job Count")
    pipeline_external_id = fields.Char("External ID")
    web_url = fields.Char(string="Pipeline URL")

    def _compute_job_count(self):
        for pipeline in self:
            pipeline.job_count = len(self.job_ids.ids)

    def action_jobs(self):
        self.ensure_one()
        return {
            "res_model": "gitlab.job",
            "type": "ir.actions.act_window",
            "name": _("Gitlab Jobs"),
            "domain": [("pipeline_id", "=", self.id)],
            "views": [
                (
                    self.env.ref("gitlab_pipeline_trigger.gitlab_job_tree").id,
                    "tree",
                ),
                (
                    self.env.ref("gitlab_pipeline_trigger.gitlab_job_form").id,
                    "form",
                ),
            ],
            "view_mode": "tree,form",
            "context": {"default_pipeline_id": self.id},
        }
