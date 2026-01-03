# Django Dans Notifications

[![Lint](https://github.com/dan1229/django_dans_notifications/actions/workflows/python-lint.yml/badge.svg)](https://github.com/dan1229/django_dans_notifications/actions/workflows/python-lint.yml)
[![Test](https://github.com/dan1229/django_dans_notifications/actions/workflows/python-test.yml/badge.svg)](https://github.com/dan1229/django_dans_notifications/actions/workflows/python-test.yml)
[![Types](https://github.com/dan1229/django_dans_notifications/actions/workflows/python-types.yml/badge.svg)](https://github.com/dan1229/django_dans_notifications/actions/workflows/python-types.yml)
[![codecov](https://codecov.io/gh/dan1229/django_dans_notifications/branch/main/graph/badge.svg?token=TL09HDQWBJ)](https://codecov.io/gh/dan1229/django_dans_notifications)

[![Python Versions](https://img.shields.io/pypi/pyversions/django-dans-notifications.svg?color=3776AB&logo=python&logoColor=white)](https://www.python.org/)
[![Django Versions](https://img.shields.io/pypi/djversions/django-dans-notifications?color=0C4B33&logo=django&logoColor=white&label=django)](https://www.djangoproject.com/)
[![PyPI Version](https://img.shields.io/pypi/v/django_dans_notifications.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/django-dans-notifications/)
[![Downloads](https://static.pepy.tech/badge/django-dans-notifications/month)](https://pepy.tech/project/django-dans-notifications)
[![License](https://img.shields.io/pypi/l/django-dans-notifications.svg?color=blue)](https://github.com/dan1229/django-dans-notifications/blob/main/LICENSE.txt)
[![Codacy grade](https://img.shields.io/codacy/grade/21cb657283c04e70b56fb935277a1ad1?logo=codacy)](https://www.codacy.com/app/dan1229/django-dans-notifications)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg?logo=python&logoColor=black)](https://github.com/psf/black)

## Description

A Django app to handle notifications.

Support for basic notifications, push notifications, and email notifications.

[Available on PyPi](https://pypi.org/project/django-dans-notifications/)

## Quick start

1. Install the package via pip:

```bash
pip install django-dans-notifications
```

2. Add "django_dans_notifications" to your INSTALLED_APPS setting like this:

```python
INSTALLED_APPS = [
	...
	'django_dans_notifications',
]
```

3. Include the URL configs in your project `urls.py` for the REST API endpoints like this:

```python
path("api/notifications/", include("django_dans_notifications.urls")),
```

4. Run `python manage.py migrate` to update your database schema.

5. Use the API endpoints, in code or your Django admin portal.

### Requirements

- Python 3.8 or higher
- Django 3.1 or higher
- Django Rest Framework
  - **NOTE:** not only must you have this installed, you must have set `DEFAULT_AUTHENTICATION_CLASSES` and `DEFAULT_PAGINATION_CLASS` in your `settings.py` to work with the APIs properly. An example config would be:

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
}
```


### Available Settings

Currently all available settings are optional:

- `TEAM_NAME` - Default team name to use for emails, can be added to message context manually as well still.
- `IN_TEST` - Whether running in tests or not. Used to determine whether to actually send email (when True, emails are not sent).

#### Email Threading Settings (Optional)
The app now uses an improved threading system for sending emails asynchronously with the following optional settings:

- `EMAIL_MAX_WORKERS` - Maximum number of concurrent threads for sending emails. Default: `3`
- `EMAIL_MAX_RETRIES` - Number of retry attempts for failed email sends. Default: `3`
- `EMAIL_RETRY_DELAY` - Base delay in seconds between retry attempts (uses exponential backoff). Default: `1.0`
- `EMAIL_SYNC_MODE` - Set to `True` to disable threading entirely (useful for debugging). Default: `False`

Add these to your `settings.py` file to customize the app's behavior like so:

```python
# Basic settings
TEAM_NAME = "My Team"
IN_TEST = True  # Emails won't be sent when True

# Optional: Email threading configuration
EMAIL_MAX_WORKERS = 5  # Allow up to 5 concurrent email threads
EMAIL_MAX_RETRIES = 5  # Try up to 5 times for failed sends
EMAIL_RETRY_DELAY = 2.0  # Start with 2 second delay between retries
EMAIL_SYNC_MODE = False  # Use async mode (set True for synchronous sending)
```

**Note:** The email threading system is fully backward compatible. If you don't specify these settings, sensible defaults will be used.

## Features

### Models

- **NotificationEmail**: Handles email notifications.
- **NotificationBasic**: Handles basic notifications.
- **NotificationPush**: Handles push notifications.

### Managers

- **NotificationEmailManager**: Handles sending and managing email notifications.
- **NotificationBasicManager**: Handles basic notifications.
- **NotificationPushManager**: Handles push notifications.

### API ViewSets

- **NotificationEmailViewSet**: API endpoints for email notifications.
- **NotificationBasicViewSet**: API endpoints for basic notifications.
- **NotificationPushViewSet**: API endpoints for push notifications.

### Utility Classes

- **NotificationManager**: Exposes common functionality and maintains object permissions.
  - Methods: `get_notifications_push/email/basic/all`, `mark_notification_basic_read`.

## Usage

The main way to interact with this app is to create and use the appropriate models and their managers' methods as needed.

Also included is the `NotificationManager` class to expose some common functionality and maintain object permissions.

Some of its methods currently are:

- `get_notifications_push/email/basic/all`
    - Enforce object ownership and notification 'direction'
- `mark_notification_basic_read`

You can also interact directly, so for example to send an email notification:

```python
from django_dans_notifications.models.notifications import NotificationEmail

email_notification = NotificationEmail.objects.send_email(
    subject="Hello",
    template="django-dans-emails/default.html",
    sender="sender@example.com",
    recipients=["recipient@example.com"],
    context={"user": "John Doe"},
    file_attachment=None
)
```

## Docs

#### [Model docs](https://github.com/dan1229/django_dans_notifications/tree/main/docs/models.md).

#### [API docs](https://github.com/dan1229/django_dans_notifications/tree/main/docs/apis.md).

#### [Email Template docs](https://github.com/dan1229/django_dans_notifications/tree/main/docs/email-templates.md).

#### [Email Threading docs](https://github.com/dan1229/django_dans_notifications/tree/main/docs/email-threading.md).

-------------------------------------------------------

##### [https://danielnazarian.com](https://danielnazarian.com)

##### Copyright 2024 © Daniel Nazarian.

