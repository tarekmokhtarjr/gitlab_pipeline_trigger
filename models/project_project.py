from odoo import models, fields

class Project(models.Model):
    _inherit = 'project.project'
    
    custom_pipeline_runner_ids = fields.One2many('gitlab.pipeline.runner', 'project_id', string='Custom Gitlab Pipeline Runner')
    project_namespace = fields.Char('Project Namespace')