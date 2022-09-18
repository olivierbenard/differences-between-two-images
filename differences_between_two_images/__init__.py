"""
Module defining the Log Level.
"""

import logging
from dynaconf import settings

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
