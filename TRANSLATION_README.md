# legal practice management - Arabic Translation Implementation

## Overview

This document describes the complete Arabic translation implementation for the legal practice management module, following Odoo's highest standards and best practices.

## Translation Files Structure

```
legal_practice_management/
├── i18n/
│   ├── legal_practice_management.pot    # Translation template
│   └── ar.po                       # Arabic translation file
```

## Implementation Details

### 1. Translation Template (.pot file)

The `legal_practice_management.pot` file contains all translatable strings from the module, including:
- Field labels and help text
- Selection field options
- View labels and group names
- Menu items

### 2. Arabic Translation (.po file)

The `ar.po` file provides complete Arabic translations for all strings, including:
- Professional legal terminology
- Proper Arabic grammar and context
- Consistent terminology throughout the module

## Translated Elements

### Model Fields (Project)

| English | Arabic |
|---------|--------|
| File Number in the Office | رقم الملف في المكتب |
| Court Name | اسم المحكمة |
| Court Circle | دائرة المحكمة |
| Case Filing Date | تاريخ رفع الدعوى |
| First Degree Case Number | رقم الدعوى في الدرجة الأولى |
| Second Degree Case Number | رقم الدعوى في الدرجة الثانية |
| Client Status | حالة العميل |
| Opponent Status | حالة الخصم |
| Opponent's Name | اسم الخصم |
| Opponent's Address | عنوان الخصم |
| Opponent's Phone Number | رقم هاتف الخصم |
| Opponent's Attorney's Name | اسم محامي الخصم |
| Opponent's Attorney's Phone | هاتف محامي الخصم |

### Model Fields (Partner/Lead)

| English | Arabic |
|---------|--------|
| Client Open Date | تاريخ فتح العميل |
| Name in English | الاسم بالإنجليزية |
| Nationality | الجنسية |
| Residence Country | بلد الإقامة |
| National ID | رقم الهوية الوطنية |
| Passport Number | رقم جواز السفر |
| Birth Date | تاريخ الميلاد |
| Sex | الجنس |
| Preferred Language | اللغة المفضلة |
| Communication Preferences | تفضيلات التواصل |
| Representative | الممثل |
| Representative Title | لقب الممثل |
| Entity Type | نوع الكيان |
| Commercial Register No. | رقم السجل التجاري |
| Tax Registration Number | رقم التسجيل الضريبي |
| Company Activity | نشاط الشركة |

### Selection Options

| English | Arabic |
|---------|--------|
| Arabic | العربية |
| English | الإنجليزية |
| French | الفرنسية |
| Other | أخرى |
| LLC | شركة ذات مسؤولية محدودة |
| JSC | شركة مساهمة |
| Partnership | شركة تضامن |
| Male | ذكر |
| Female | أنثى |

### View Labels

| English | Arabic |
|---------|--------|
| Legal Case Details | تفاصيل القضية القانونية |
| Case Identification | تعريف القضية |
| Client Details | تفاصيل العميل |
| Opponent Details | تفاصيل الخصم |
| Cases & Matters | القضايا والمسائل |
| Matters | المسائل القانونية |
| Client Information | معلومات العميل |
| General | عام |
| Personal (Individual) | شخصي (فرد) |
| Company | شركة |

## Best Practices Implemented

### 1. Translation Function Usage
All translatable strings are properly wrapped with the `_()` function:
```python
from odoo import models, fields, _

field_name = fields.Char(string=_("Field Label"))
```

### 2. Selection Field Translation
Selection options are properly translated:
```python
LANGUAGE_SELECTION = [
    ('ar', _('Arabic')),
    ('en', _('English')),
    ('fr', _('French')),
    ('other', _('Other')),
]
```

### 3. View String Translation
View strings are automatically translated by Odoo's translation system:
```xml
<page string="Legal Case Details">
<group string="Case Identification">
```

### 4. Proper Plural Forms
Arabic translation includes proper plural forms configuration:
```
"Plural-Forms: nplurals=6; plural=n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : n%100>=11 ? 4 : 5;\n"
```

## Installation and Usage

### 1. Install the Module
```bash
# Update the module list
./odoo-bin -u legal_practice_management -d your_database
```

### 2. Enable Arabic Language
1. Go to Settings > Translations > Languages
2. Install Arabic language if not already installed
3. Set Arabic as the user's language

### 3. Update Translations
```bash
# Update translations for the module
./odoo-bin -u legal_practice_management -d your_database --i18n-overwrite
```

## Quality Assurance

### Translation Quality
- All translations reviewed for accuracy
- Legal terminology verified with Arabic legal experts
- Consistent terminology throughout the module
- Proper Arabic grammar and context

### Technical Standards
- Follows Odoo translation standards
- Proper use of `_()` function
- Correct plural forms configuration
- UTF-8 encoding maintained

## Maintenance

### Adding New Translations
1. Add new strings with `_()` function in Python files
2. Add string attributes in XML files
3. Update the .pot file: `./odoo-bin -u legal_practice_management --i18n-export=addons/legal_practice_management/i18n/legal_practice_management.pot`
4. Update the .po file with new translations
5. Compile translations: `./odoo-bin -u legal_practice_management --i18n-overwrite`

### Updating Existing Translations
1. Modify the .po file with updated translations
2. Compile translations: `./odoo-bin -u legal_practice_management --i18n-overwrite`
3. Restart Odoo server

## Support

For translation issues or improvements:
- Contact: Mohamed Essam (mohamed@essamsalem.com)
- Repository: https://essamsalem.com
- License: LGPL-3

## Version History

- v1.0: Initial Arabic translation implementation
  - Complete field translations
  - Selection option translations
  - View label translations
  - Menu item translations
  - Professional legal terminology 