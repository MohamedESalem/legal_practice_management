from odoo import api, fields, models
from odoo.osv import expression

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
    def _get_context_pipeline_type(self):
        pipeline_type = (
            self.env.context.get('pipeline_board_type')
            or self.env.context.get('default_pipeline_type')
        )
        if pipeline_type in dict(PIPELINE_TYPE_SELECTION):
            return pipeline_type

        if self.env.context.get('active_model') == 'project.project':
            active_project_id = self.env.context.get('active_id') or self.env.context.get('default_project_id')
            if active_project_id:
                project = self.env['project.project'].browse(active_project_id).exists()
                if project and project.pipeline_type in dict(PIPELINE_TYPE_SELECTION):
                    return project.pipeline_type

        if self.env.context.get('create_from_cases'):
            return 'litigation'
        if self.env.context.get('create_from_matters'):
            return 'legal_subject'
        return False

    @api.model
    def _default_pipeline_type(self):
        pipeline_type = self._get_context_pipeline_type()
        if pipeline_type:
            return pipeline_type
        return DEFAULT_PIPELINE_TYPE

    @api.model
    def _read_group_expand_full(self, groups, domain):
        pipeline_type = self._get_context_pipeline_type()
        if pipeline_type in dict(PIPELINE_TYPE_SELECTION):
            return groups.search([('pipeline_type', '=', pipeline_type)])
        return super()._read_group_expand_full(groups, domain)

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, **kwargs):
        domain = list(domain or [])
        pipeline_type = self._get_context_pipeline_type()
        has_pipeline_filter = any(
            isinstance(item, (list, tuple))
            and len(item) >= 1
            and item[0] == 'pipeline_type'
            for item in domain
        )

        if pipeline_type and not has_pipeline_filter:
            domain = expression.AND([domain, [('pipeline_type', '=', pipeline_type)]])

        return super()._search(
            domain,
            offset=offset,
            limit=limit,
            order=order,
            **kwargs,
        )
