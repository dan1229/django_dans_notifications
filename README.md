# Django Dans Notifications

[![Lint](https://github.com/dan1229/django_dans_notifications/actions/workflows/lint.yml/badge.svg)](https://github.com/dan1229/django_dans_notifications/actions/workflows/lint.yml)
[![Test Python](https://github.com/dan1229/django_dans_notifications/actions/workflows/test-python.yml/badge.svg)](https://github.com/dan1229/django_dans_notifications/actions/workflows/test-python.yml)
[![codecov](https://codecov.io/gh/dan1229/django_dans_notifications/branch/main/graph/badge.svg?token=TL09HDQWBJ)](https://codecov.io/gh/dan1229/django_dans_notifications)

## Description

A Django app to handle notifications.

Support for basic notifications, push notifications and email notifications.

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
- `IN_TEST` - Whether running in tests or not. Used to determine whether to actually send email.

Add these to your `settings.py` file to customize the app's behavior like so:

```python
TEAM_NAME = "My Team"
IN_TEST = True
```


## Usage

The main way to interact with this app is to create and use the appropriate models and their managers' methods as needed.

Also included is the `NotificationManager` a class to expose some common functionality and maintain object permissions.

Some of its methods currently are:

- get_notifications_push/email/basic/all
    - Enforce object ownership and notification 'direction'
- mark_notification_basic_read

You can also interact directly, so for example to send an email notification:

```python
from django_dans_notifications.models import EmailNotification

email_notification = EmailNotification.objects.send_email(...)
```

## Docs

#### [Model docs](https://github.com/dan1229/django_dans_notifications/tree/main/docs/models.md).

#### [API docs](https://github.com/dan1229/django_dans_notifications/tree/main/docs/apis.md).

#### [Email Template docs](https://github.com/dan1229/django_dans_notifications/tree/main/docs/email-templates.md).

-------------------------------------------------------

##### [https://danielnazarian.com](https://danielnazarian.com)

##### Copyright 2024 © Daniel Nazarian.

