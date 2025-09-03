from . import models

# Import post_init_hook into the module’s root namespace.
# Odoo requires this so it can find and execute the hook after installation.
from .hooks import post_init_hook