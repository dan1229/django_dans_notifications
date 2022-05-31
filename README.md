# Django Dans Notifications

[![Test Python](https://github.com/dan1229/django_dans_notifications/actions/workflows/test_python.yml/badge.svg)](https://github.com/dan1229/django_dans_notifications/actions/workflows/test_python.yml)
[![Lint](https://github.com/dan1229/django_dans_notifications/actions/workflows/lint.yml/badge.svg)](https://github.com/dan1229/django_dans_notifications/actions/workflows/lint.yml)

#### [GitHub](https://github.com/dan1229/django_dans_notifications)

#### [PyPi](https://pypi.org/project/django-dans-notifications/)

## Description

A Django app to handle notifications.

## Quick start

1. Add "notifications" to your INSTALLED_APPS setting like this:

```python
INSTALLED_APPS = [
	...
	'notifications',
]
```

2. Include the notifications URLconf in your project urls.py like this:

```python
path("notifications/", include("notifications.urls")),
```

3. Run `python manage.py migrate` to create the models.

4. Create notifications via the API endpoints, in code or your Admin portal.

### Requirements

- Python 3.0 or higher
- Django 3.0 or higher
- Django Rest Framework

## Models

To use this package simply utilize the models included as well as their properties/helper methods.

The included models are:

- `NotificationEmail`
    - Meant to track emails sent.
    - Email templates included, editable via context variables
        - `NotificationEmailTemplate` model - see template docs at the end of this file
        - Admin editable
        - User editable coming soon!
    - send_email function to actually send emails and handle object creation.
        - `NotificationEmail.objects.send_email(...)`
- `NotificationBasic`
    - Meant to model a generic notification stack internal to the application.
    - Have a 'read' property
- `NotificationPush`
    - Track push notifications that may require extra information


ALL notifications inherit from `NotificationBase` and thus all have the following properties:
- `recipients` - comma separated list of emails the notification was sent to.
- `sender` - email of the sending user.
- `datetime_sent` - date time the notification was sent.
- `sent_successfully` - whether the notification was processed correctly.


## Usage

The main way to interact with this app is to create and use the appropriate models and their managers' methods as needed.

Also included is the `NotificationManager` a class to expose some common functionality and maintain object permissions.

Some available methods currently are:

- get_notifications_push/email/basic/all
    - Enforce object ownership and notification 'direction'
- mark_notification_basic_read

### APIs

See [API docs](./docs/apis.md).

### Email Templates

See [Email Template docs](./docs/email-templates.md).
