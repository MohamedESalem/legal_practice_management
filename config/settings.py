# -*- coding: utf-8 -*-
"""
Legal Case Management Configuration
Centralized configuration settings.
"""

# Module configuration
MODULE_NAME = 'legal_case_management'
MODULE_VERSION = '1.0'
MODULE_AUTHOR = 'Mohamed Essam'
MODULE_WEBSITE = 'https://essamsalem.com'

# Translation configuration
SUPPORTED_LANGUAGES = ['en', 'ar', 'fr']
DEFAULT_LANGUAGE = 'en'

# Legal case configuration
CASE_NUMBER_PREFIX = 'LC'
CASE_NUMBER_SEQUENCE = 'legal.case.sequence'

# Field groups
LEGAL_CASE_FIELDS = [
    'office_file_number',
    'court_name',
    'court_circle',
    'lawsuit_filing_date',
    'first_degree_case_number_year',
    'second_degree_case_number_year',
    'client_status',
    'opponent_status',
    'opponent_name',
    'opponent_address',
    'opponent_phone',
    'opponent_attorney_name',
    'opponent_attorney_phone',
]

CLIENT_FIELDS = [
    'x_client_open_date',
    'x_name_en',
    'x_nationality',
    'x_residence_country',
    'x_national_id',
    'x_passport_number',
    'x_birth_date',
    'x_sex',
    'x_preferred_language',
    'x_communication_preferences',
    'x_representative',
    'x_representative_title',
    'x_entity_type',
    'x_commercial_register_no',
    'x_tax_registration_number',
    'x_company_activity',
] 