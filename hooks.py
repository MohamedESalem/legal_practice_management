import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

# post_init_hook is a special Odoo hook function that runs automatically
# right after the module is installed (but before first usage).
#
# Why we use it:
# - It allows us to run cleanup or customization logic immediately after install.
# - In this case, we need to make sure the 'sale_project' module is removed.
#
# Why we uninstall 'sale_project':
# - 'sale_project' automatically links Sales Orders with Projects.
# - In Legal Practice Management, projects represent legal cases, not sales orders.
# - Keeping 'sale_project' would create unwanted dependencies and behaviors,
#   so we ensure it’s uninstalled cleanly at module setup.
def post_init_hook(env):
    """Automatically uninstall sale_project right after module installation."""
    module = env['ir.module.module'].search([('name', '=', 'sale_project')], limit=1)
    if module and module.state == 'installed':
        _logger.info("Uninstalling 'sale_project' via post_init_hook.")
        module.button_uninstall()
    else:
        _logger.info("'sale_project' module is not installed.")