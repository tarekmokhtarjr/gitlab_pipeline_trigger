from odoo import models, fields, Command, _
from odoo.exceptions import ValidationError
import gitlab


class GitlabPipelineRunner(models.Model):
    _name = "gitlab.pipeline.runner"
    _description = "Gitlab Pipeline Runners"

    branch = fields.Char("Branch")
    name = fields.Char("Name")
    project_id = fields.Many2one("project.project", string="Project")
    pipeline_ids = fields.One2many(
        "gitlab.pipeline", "gitlab_runner_id", string="Pipelines"
    )
    project_namespace = fields.Char("Project Namespace")
    pipeline_variable_ids = fields.One2many(
        "pipeline.variable", "gitlab_runner_id", string="Pipeline Variables"
    )
    pipeline_count = fields.Integer(
        compute="_compute_pipeline_count", string="Pipeline Count"
    )

    def _compute_pipeline_count(self):
        """Computes the number of pipelines which are created by this
        runner."""
        for gl_runner in self:
            gl_runner.pipeline_count = len(self.pipeline_ids.ids)

    def action_pipelines(self):
        """Pipelines action.

        :return: action dictionary
        :rtype: dictionary
        """
        self.ensure_one()
        return {
            "res_model": "gitlab.pipeline",
            "type": "ir.actions.act_window",
            "name": _("Gitlab Pipelines"),
            "domain": [("gitlab_runner_id", "=", self.id)],
            "views": [
                (
                    self.env.ref(
                        "gitlab_pipeline_trigger.gitlab_pipeline_tree"
                    ).id,
                    "tree",
                ),
                (
                    self.env.ref(
                        "gitlab_pipeline_trigger.gitlab_pipeline_form"
                    ).id,
                    "form",
                ),
            ],
            "view_mode": "tree,form",
            "context": {"default_gitlab_runner_id": self.id},
        }

    def validate_config_on_create(self, gitlab_url, gitlab_private_token):
        """Authenticates the gitlab url and the token.

        :param gitlab_url: Gitlab server url, example gitlab.com
        :type gitlab_url: string
        :param gitlab_private_token: Gitlab private token
        :type gitlab_private_token: string
        :raises ValidationError: An error message which appears if the gitlab
                token or the url is not correct.
        """
        try:
            gl = gitlab.Gitlab(
                url=gitlab_url, private_token=gitlab_private_token
            )
            gl.auth()
        except:
            raise ValidationError(
                "Invalid gitlab token or url, please provide the correct "
                "private token and gitlab url."
            )

    def run_pipeline(self):
        """Create and run the pipeline and it's related jobs.

        :return: dictionary for pipeline action
        :rtype: dictionary
        """
        enabled = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("gitlab_pipeline_trigger.enable_gitlab_integration")
        )
        gitlab_url = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("gitlab_pipeline_trigger.gitlab_url")
        )
        gitlab_private_token = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("gitlab_pipeline_trigger.gitlab_private_token")
        )
        self.validate_config_on_create(gitlab_url, gitlab_private_token)
        if enabled:
            gl = gitlab.Gitlab(
                url=gitlab_url, private_token=gitlab_private_token
            )
            project = gl.projects.get(self.project_namespace)
            # Note: if there is no .gitlab-ci.yml an error
            # (Missing CI config file) will raise
            pipeline = project.pipelines.create(
                {
                    "ref": self.branch,
                    "variables": [
                        {"key": variable.key, "value": variable.value}
                        for variable in self.pipeline_variable_ids
                    ],
                }
            )
            gl_pipeline = self.env["gitlab.pipeline"].create(
                {
                    "gitlab_runner_id": self.id,
                    "pipeline_external_id": pipeline._attrs.get("id"),
                    "web_url": pipeline._attrs.get("web_url"),
                }
            )
            gl_pipeline.job_ids = [
                Command.create(
                    {
                        "name": job._attrs.get("name"),
                        "job_external_id": job._attrs.get("id"),
                        "pipeline_id": gl_pipeline.id,
                        "web_url": job._attrs.get("web_url"),
                    }
                )
                for job in pipeline.jobs.list()
            ]
            self.pipeline_ids = [Command.link(gl_pipeline.id)]
            action = {
                "name": _("Gitlab Pipeline"),
                "type": "ir.actions.act_window",
                "res_model": "gitlab.pipeline",
                "views": [
                    [
                        self.env.ref(
                            "gitlab_pipeline_trigger.gitlab_pipeline_form"
                        ).id,
                        "form",
                    ]
                ],
                "res_id": gl_pipeline.id,
            }
            return action
