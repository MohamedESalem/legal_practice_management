# Merged from crm_client_fields v1.0 on 2025-07-30 by Mohamed Essam
from odoo import models, fields, _

LANGUAGE_SELECTION = [
    ('ar', 'Arabic'),
    ('en', 'English'),
    ('fr', 'French'),
    ('other', 'Other'),
]
ENTITY_TYPE_SELECTION = [
    ('llc', 'LLC'),
    ('jsc', 'JSC'),
    ('partnership', 'Partnership'),
    ('other', 'Other'),
]
SEX_SELECTION = [
    ('male', 'Male'),
    ('female', 'Female')
]

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    x_client_open_date = fields.Date(string='Client Open Date')
    x_name_en = fields.Char(string='Name in English')
    x_nationality = fields.Many2one('res.country', string='Nationality')
    x_residence_country = fields.Many2one('res.country', string='Residence Country')
    x_national_id = fields.Char(string='National ID')
    x_passport_number = fields.Char(string='Passport Number')
    x_birth_date = fields.Date(string='Birth Date')
    x_sex = fields.Selection(SEX_SELECTION, string='Sex')
    x_preferred_language = fields.Selection(LANGUAGE_SELECTION, string='Preferred Language')
    x_communication_preferences = fields.Text(string='Communication Preferences')
    x_representative = fields.Char(string='Representative')
    x_representative_title = fields.Char(string='Representative Title')
    x_entity_type = fields.Selection(ENTITY_TYPE_SELECTION, string='Entity Type')
    x_commercial_register_no = fields.Char(string='Commercial Register No.')
    x_tax_registration_number = fields.Char(string='Tax Registration Number')
    x_company_activity = fields.Char(string='Company Activity') 