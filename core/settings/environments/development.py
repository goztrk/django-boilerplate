"""
Django Settings Environment Override
"""
# Application Imports
from core.settings.components.templates import TEMPLATES


DEBUG = True
TEMPLATE_DEBUG = True

TEMPLATES[0]["OPTIONS"]["debug"] = TEMPLATE_DEBUG
