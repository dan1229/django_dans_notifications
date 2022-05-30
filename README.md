# Django Dans Notifications

[![Test Django](https://github.com/dan1229/django_dans_notifications/actions/workflows/test-django.yml/badge.svg)](https://github.com/dan1229/django_dans_notifications/actions/workflows/test-django.yml)

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

2. Include the notifications URLconf in your project urls.py like this::

   path("notifications/", include("notifications.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Create notifications via the API or Admin portal.

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

## Usage

The main way to interact with this app is to create and use the appropriate models and their managers' methods as needed.

Also included is the `NotificationManager` a class to expose some common functionality and maintain object permissions.

Some available methods currently are:

- get_notifications_push/email/basic/all
    - Enforce object ownership and notification 'direction'
- mark_notification_basic_read

### APIs

See `docs/apis.md`.

### Email Templates

See `docs/email-templates.md`.