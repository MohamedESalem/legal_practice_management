# legal practice management

Transform Odoo Projects into Cases & Matters for law firms with full Arabic support.

## Features

- ✅ Complete Arabic translation support
- ✅ Professional legal terminology
- ✅ Dynamic menu translations
- ✅ Centralized constants and configuration
- ✅ Comprehensive test suite
- ✅ Well-documented codebase

## Quick Start

1. **Install the module**:
   ```bash
   ./odoo-bin -u legal_practice_management -d your_database
   ```

2. **Enable Arabic language**:
   - Go to Settings > Translations > Languages
   - Install Arabic language
   - Set Arabic as user language

3. **Update translations**:
   ```bash
   ./odoo-bin -u legal_practice_management -d your_database --i18n-overwrite
   ```

## Documentation

- [Development Guide](docs/DEVELOPMENT_GUIDE.md) - Comprehensive development guide
- [Translation README](TRANSLATION_README.md) - Translation implementation details
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - Implementation overview

## Testing

Run the comprehensive test suite:
```bash
cd addons/legal_practice_management
python tests/test_translations.py
```

## Support

- **Contact**: Mohamed Essam (mohamed@essamsalem.com)
- **Repository**: https://essamsalem.com
- **License**: LGPL-3 