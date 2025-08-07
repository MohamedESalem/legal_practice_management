# -*- coding: utf-8 -*-
"""
legal practice management - Partner Extensions
Extends res.partner with legal practice management fields.
"""

from odoo import models, fields, _
from .constants import LANGUAGE_SELECTION, ENTITY_TYPE_SELECTION, SEX_SELECTION

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Legal Case Partner'

    x_client_open_date = fields.Date(string=_('Client Open Date'))
    x_name_en = fields.Char(string=_('Name in English'))
    x_nationality = fields.Many2one('res.country', string=_('Nationality'))
    x_residence_country = fields.Many2one('res.country', string=_('Residence Country'))
    x_national_id = fields.Char(string=_('National ID'))
    x_passport_number = fields.Char(string=_('Passport Number'))
    x_birth_date = fields.Date(string=_('Birth Date'))
    x_sex = fields.Selection(SEX_SELECTION, string=_('Sex'))
    x_preferred_language = fields.Selection(LANGUAGE_SELECTION, string=_('Preferred Language'))
    x_communication_preferences = fields.Text(string=_('Communication Preferences'))
    x_representative = fields.Char(string=_('Representative'))
    x_representative_title = fields.Char(string=_('Representative Title'))
    x_entity_type = fields.Selection(ENTITY_TYPE_SELECTION, string=_('Entity Type'))
    x_commercial_register_no = fields.Char(string=_('Commercial Register No.'))
    x_tax_registration_number = fields.Char(string=_('Tax Registration Number'))
    x_company_activity = fields.Char(string=_('Company Activity')) 