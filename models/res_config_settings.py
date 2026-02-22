# -*- coding: utf-8 -*-
"""
Legal Practice Management Configuration Settings
Administrator-controlled template configuration for automatic matter separation.
"""

from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Template Configuration Fields
    litigation_template_id = fields.Many2one(
        'project.project',
        string='Litigation Template',
        domain=[('is_template', '=', True), ('pipeline_type', '=', 'litigation')],
        config_parameter='legal_practice_management.litigation_template_id',
        help='Template to use when creating Legal Cases (litigation matters)'
    )

    advisory_template_id = fields.Many2one(
        'project.project',
        string='Advisory Template',
        domain=[('is_template', '=', True), ('pipeline_type', '=', 'legal_subject')],
        config_parameter='legal_practice_management.advisory_template_id',
        help='Template to use when creating Legal Subjects (advisory matters)'
    )
