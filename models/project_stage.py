from odoo import api, fields, models

from .constants import DEFAULT_PIPELINE_TYPE, PIPELINE_TYPE_SELECTION


class ProjectProjectStage(models.Model):
    _inherit = 'project.project.stage'

    pipeline_type = fields.Selection(
        PIPELINE_TYPE_SELECTION,
        string='Pipeline Type',
        required=True,
        default=lambda self: self._default_pipeline_type(),
        index=True,
    )

    @api.model
    def _default_pipeline_type(self):
        pipeline_type = (
            self.env.context.get('pipeline_board_type')
            or self.env.context.get('default_pipeline_type')
        )
        allowed_values = dict(PIPELINE_TYPE_SELECTION)
        if pipeline_type in allowed_values:
            return pipeline_type
        if self.env.context.get('create_from_cases'):
            return 'litigation'
        if self.env.context.get('create_from_matters'):
            return 'legal_subject'
        return DEFAULT_PIPELINE_TYPE

    @api.model
    def _read_group_expand_full(self, groups, domain):
        pipeline_type = (
            self.env.context.get('pipeline_board_type')
            or self.env.context.get('default_pipeline_type')
        )
        if pipeline_type in dict(PIPELINE_TYPE_SELECTION):
            return groups.search([('pipeline_type', '=', pipeline_type)])
        return super()._read_group_expand_full(groups, domain)
