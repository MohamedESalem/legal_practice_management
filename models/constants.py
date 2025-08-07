# -*- coding: utf-8 -*-
"""
legal practice management Constants
Centralized constants and selection options.
"""

from odoo import _

# Language selection options
LANGUAGE_SELECTION = [
    ('ar', _('Arabic')),
    ('en', _('English')),
    ('fr', _('French')),
    ('other', _('Other')),
]

# Entity type selection options
ENTITY_TYPE_SELECTION = [
    ('llc', _('LLC')),
    ('jsc', _('JSC')),
    ('partnership', _('Partnership')),
    ('other', _('Other')),
]

# Sex selection options
SEX_SELECTION = [
    ('male', _('Male')),
    ('female', _('Female'))
]

# Client status options
CLIENT_STATUS_SELECTION = [
    ('plaintiff', _('Plaintiff')),
    ('defendant', _('Defendant')),
    ('third_party', _('Third Party')),
    ('witness', _('Witness')),
    ('other', _('Other')),
]

# Case type options
CASE_TYPE_SELECTION = [
    ('civil', _('Civil')),
    ('criminal', _('Criminal')),
    ('commercial', _('Commercial')),
    ('family', _('Family')),
    ('administrative', _('Administrative')),
    ('other', _('Other')),
] 