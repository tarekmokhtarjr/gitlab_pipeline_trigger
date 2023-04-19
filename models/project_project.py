from odoo import models, fields, _


class Project(models.Model):
    _inherit = "project.project"

    custom_pipeline_runner_ids = fields.One2many(
        "gitlab.pipeline.runner",
        "project_id",
        string="Custom Gitlab Pipeline Runner",
    )
    project_namespace = fields.Char("Project Namespace")
    gitlab_runner_count = fields.Integer(
        compute="_compute_gitlab_runner_count", string="Gitlab Runner Count"
    )

    def _compute_gitlab_runner_count(self):
        """Counts the number of related Gitlab runners for the project."""
        for project in self:
            project.gitlab_runner_count = len(
                self.custom_pipeline_runner_ids.ids
            )

    def action_gitlab_runners(self):
        """Returns a dictionary for gitlab runners action.

        :return: dictionary for gitlab runners action.
        :rtype: dictionary
        """
        self.ensure_one()
        return {
            "res_model": "gitlab.pipeline.runner",
            "type": "ir.actions.act_window",
            "name": _("Gitlab Runners"),
            "domain": [("project_id", "=", self.id)],
            "views": [
                (
                    self.env.ref(
                        "gitlab_pipeline_trigger.gitlab_pipeline_runner_tree"
                    ).id,
                    "tree",
                ),
                (
                    self.env.ref(
                        "gitlab_pipeline_trigger.gitlab_pipeline_runner_form"
                    ).id,
                    "form",
                ),
            ],
            "view_mode": "tree,form",
            "context": {"default_project_id": self.id},
        }
