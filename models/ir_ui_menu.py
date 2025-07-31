from odoo import models, fields, api, _

class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def _get_menu_name(self, menu_id):
        """Get the translated menu name based on the current language"""
        menu = self.browse(menu_id)
        if menu.name == "Cases & Matters":
            return _("Cases & Matters")
        return menu.name

    def get_menu_name(self):
        """Return the translated menu name"""
        return self._get_menu_name(self.id) 