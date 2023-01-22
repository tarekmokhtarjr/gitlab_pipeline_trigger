from odoo import models, fields
from odoo.exceptions import ValidationError
import gitlab


class GitlabPipelineRunner(models.Model):
    _name = 'gitlab.pipeline.runner'
    _description = 'Gitlab Pipeline Runners'

    project_id = fields.Many2one('project.project', string='Project')
    pipeline_ids = fields.One2many(
        'gitlab.pipeline', 
        'gitlab_runner_id', 
        string='Pipelines'
    )
    project_namespace = fields.Char('Project URL', related='project_id.project_namespace')
    branch = fields.Char('Branch')
    pipeline_variable_ids = fields.One2many(
        'pipeline.variable', 
        'gitlab_runner_id', 
        string='Pipeline Variables'
    )

    def validate_config_on_create(self, gitlab_url, gitlab_private_token):
        try:
            gl = gitlab.Gitlab(
                    url=gitlab_url, 
                    private_token=gitlab_private_token
                )
            gl.auth()
        except:
            raise ValidationError(
                "Invalid token, please provide the correct private token.")
    
    def run_pipeline(self):
        enabled = self.env["ir.config_parameter"].sudo()\
            .get_param("gitlab_pipeline_trigger.enable_gitlab_integration")
        gitlab_url = self.env["ir.config_parameter"].sudo()\
            .get_param("gitlab_pipeline_trigger.gitlab_url")
        gitlab_private_token = self.env["ir.config_parameter"].sudo()\
            .get_param("gitlab_pipeline_trigger.gitlab_private_token")
        self.validate_config_on_create(gitlab_url, gitlab_private_token)
        if enabled:
            gl = gitlab.Gitlab(
                url=gitlab_url, 
                private_token=gitlab_private_token
            )
            project = gl.projects.get(self.project_namespace)
            pipeline = project.pipelines.create({
                'ref': self.branch, 
                'variables': [
                    {'key': variable.key, 'value': variable.value} 
                    for variable in self.pipeline_variable_ids
                ]
            })
            jobs = pipeline.jobs.list()