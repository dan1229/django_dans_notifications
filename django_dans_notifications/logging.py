# django_dans_notifications/logging.py

import logging

# Create a logger for the package
LOGGER = logging.getLogger("django_dans_notifications")

# Set default log level (optional, can be configured by the Django project settings)
LOGGER.setLevel(logging.DEBUG)

# Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Add formatter to ch
ch.setFormatter(formatter)

# Add ch to logger if it doesn't have any handlers
if not LOGGER.handlers:
    LOGGER.addHandler(ch)
