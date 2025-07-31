# Legal Case Management - Development Guide

## Overview

This guide provides comprehensive information for developing and maintaining the Legal Case Management module.

## Architecture

### Module Structure
```
legal_case_management/
├── config/
│   └── settings.py              # Configuration settings
├── data/
│   └── legal_case_data.xml      # Data definitions
├── docs/
│   └── DEVELOPMENT_GUIDE.md     # This file
├── i18n/
│   ├── legal_case_management.pot # Translation template
│   └── ar.po                    # Arabic translations
├── models/
│   ├── __init__.py
│   ├── constants.py             # Centralized constants
│   ├── legal_case_mixin.py     # Shared functionality
│   ├── project.py              # Project extensions
│   ├── res_partner.py          # Partner extensions
│   ├── crm_lead.py             # CRM lead extensions
│   └── ir_ui_menu.py           # Menu translations
├── security/
│   └── ir.model.access.csv     # Access rights
├── tests/
│   ├── __init__.py
│   └── test_translations.py    # Translation tests
├── views/
│   ├── project_views.xml       # Project views
│   ├── res_partner_view.xml    # Partner views
│   └── crm_client_fields_view.xml # CRM views
└── __manifest__.py             # Module manifest
```

## Key Components

### 1. Constants (`models/constants.py`)
Centralized selection options and constants:
- `LANGUAGE_SELECTION`
- `ENTITY_TYPE_SELECTION`
- `SEX_SELECTION`
- `CLIENT_STATUS_SELECTION`
- `CASE_TYPE_SELECTION`

### 2. Mixin (`models/legal_case_mixin.py`)
Shared functionality for legal case management:
- `get_app_menu_name()` - Returns translated menu name
- `get_legal_terminology()` - Returns legal terminology translations

### 3. Configuration (`config/settings.py`)
Module configuration settings:
- Supported languages
- Field groups
- Module metadata

## Development Guidelines

### Adding New Fields

1. **Define constants** in `models/constants.py`:
```python
NEW_SELECTION = [
    ('option1', _('Option 1')),
    ('option2', _('Option 2')),
]
```

2. **Add field to model**:
```python
from .constants import NEW_SELECTION

new_field = fields.Selection(NEW_SELECTION, string=_('New Field'))
```

3. **Update translation files**:
```bash
./odoo-bin -u legal_case_management --i18n-export=addons/legal_case_management/i18n/legal_case_management.pot
```

### Adding New Views

1. **Create view file** in `views/` directory
2. **Add to manifest** in `data` section
3. **Update translations** if needed

### Adding New Translations

1. **Mark strings** with `_()` function
2. **Update POT file**:
```bash
./odoo-bin -u legal_case_management --i18n-export=addons/legal_case_management/i18n/legal_case_management.pot
```
3. **Add translations** to `ar.po` file
4. **Compile translations**:
```bash
./odoo-bin -u legal_case_management --i18n-overwrite
```

## Testing

### Running Tests
```bash
cd addons/legal_case_management
python tests/test_translations.py
```

### Test Coverage
- Field translation marks
- Menu translations
- Translation file structure
- Arabic translation presence

## Best Practices

### Code Organization
- Use constants for selection options
- Implement mixins for shared functionality
- Centralize configuration
- Follow Odoo naming conventions

### Translation
- Always use `_()` function for translatable strings
- Keep translations consistent
- Use professional legal terminology
- Test translations thoroughly

### Documentation
- Document all public methods
- Keep README files updated
- Include usage examples
- Maintain development guides

## Troubleshooting

### Common Issues

1. **Translation not working**:
   - Check if `_()` function is used
   - Verify translation files are compiled
   - Ensure language is installed

2. **Menu not translating**:
   - Check data file structure
   - Verify menu record IDs
   - Ensure translation files include menu strings

3. **Field not appearing**:
   - Check view inheritance
   - Verify field definition
   - Ensure proper model inheritance

## Maintenance

### Regular Tasks
1. Update translation files when adding new strings
2. Test translations after changes
3. Keep documentation updated
4. Review and update constants as needed

### Version Updates
1. Update version in manifest
2. Update translation files
3. Test all functionality
4. Update documentation

## Support

For questions or issues:
- **Contact**: Mohamed Essam (mohamed@essamsalem.com)
- **Repository**: https://essamsalem.com
- **License**: LGPL-3 