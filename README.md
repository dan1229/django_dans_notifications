# Django Dans Notifications
[![Test Django](https://github.com/dan1229/django_dans_notifications/actions/workflows/test-django.yml/badge.svg)](https://github.com/dan1229/django_dans_notifications/actions/workflows/test-django.yml)

### [GitHub](https://github.com/dan1229/django_dans_notifications)
### [PyPi](https://pypi.org/project/django-dans-notifications/)

A Django app to handle notifications.


## Models

TODO

NotificationEmail
- send email

NotificationBasic

NotificationPush


## Usage

TODO

NotificationManager


## Quick start

1. Add "polls" to your INSTALLED_APPS setting like this:

```python
INSTALLED_APPS = [
    ...
    'notifications',
]
```

2. Include the polls URLconf in your project urls.py like this::

    path("notifications/", include("notifications.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Create notifications via the API or Admin portal!



