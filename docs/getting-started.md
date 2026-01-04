# Getting Started

This guide will help you get up and running with Django Dans Notifications.

## Installation

### 1. Install the Package

Install via pip:

```bash
pip install django-dans-notifications
```

### 2. Add to Installed Apps

Add "django_dans_notifications" to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ... other apps
    'django_dans_notifications',
]
```

### 3. Configure REST API URLs

Include the URL configs in your project's main `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # ... other URLs
    path("api/notifications/", include("django_dans_notifications.urls")),
]
```

### 4. Run Migrations

Update your database schema:

```bash
python manage.py migrate
```

## Requirements

### Python and Django Versions
- **Python**: 3.8 or higher
- **Django**: 3.1 or higher
- **Django Rest Framework**: Required

### Django Rest Framework Configuration

You must configure Django Rest Framework in your `settings.py`:

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
}
```

## Configuration

All settings are optional and should be added to your `settings.py`:

### Basic Settings

```python
# Team name for email templates
TEAM_NAME = "My Team"

# Set to True during testing to prevent actual email sending
IN_TEST = False
```

### Email Threading Configuration

The app uses an advanced threading system for sending emails asynchronously:

```python
# Maximum concurrent email threads (default: 3)
EMAIL_MAX_WORKERS = 5

# Retry attempts for failed sends (default: 3)
EMAIL_MAX_RETRIES = 5

# Base delay between retries in seconds (default: 1.0)
EMAIL_RETRY_DELAY = 2.0

# Disable threading for debugging (default: False)
EMAIL_SYNC_MODE = False
```

## Next Steps

- [Usage Guide](usage.md) - Code examples for all notification types
- [API Documentation](apis.md) - REST API endpoints
- [Model Documentation](models.md) - Model fields and methods
- [Email Templates](email-templates.md) - Template customization