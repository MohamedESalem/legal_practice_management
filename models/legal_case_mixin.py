# -*- coding: utf-8 -*-
"""
legal practice management Mixin
Provides common functionality for legal practice management.
"""

from odoo import models, fields, api, _

class LegalCaseMixin(models.AbstractModel):
    """Mixin class for legal practice management functionality"""
    _name = 'legal.case.mixin'
    _description = 'legal practice management Mixin'

    @api.model
    def get_app_menu_name(self):
        """Return the translated app menu name"""
        return _("Cases & Matters")

    @api.model
    def get_legal_terminology(self):
        """Return common legal terminology translations"""
        return {
            'plaintiff': _("Plaintiff"),
            'defendant': _("Defendant"),
            'third_party': _("Third Party"),
            'attorney': _("Attorney"),
            'court': _("Court"),
            'case': _("Case"),
            'matter': _("Matter"),
            'lawsuit': _("Lawsuit"),
            'filing': _("Filing"),
            'appeal': _("Appeal"),
        } 