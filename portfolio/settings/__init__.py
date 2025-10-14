"""
Django settings package
Auto-loads appropriate settings based on DJANGO_SETTINGS_MODULE environment variable
"""
import os

# Default to development settings if not specified
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'portfolio.settings.dev')

if 'prod' in settings_module:
    from .prod import *
else:
    from .dev import *