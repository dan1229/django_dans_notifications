# Django Dans Notifications
[![Test Django](https://github.com/dan1229/django_dans_notifications/actions/workflows/test-django.yml/badge.svg)](https://github.com/dan1229/django_dans_notifications/actions/workflows/test-django.yml)

### [GitHub](https://github.com/dan1229/django_dans_notifications)
### [PyPi](https://pypi.org/project/django-dans-notifications/)

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

## Models

TODO

- NotificationEmail
  - send_email
- NotificationBasic
- NotificationPush


## Usage

The main way to interact with this app is to create and use the appropriate models and their managers' methods as needed.

Also included is the `NotificationManager` a class to expose some common functionality and maintain object permissions.

Some of the available methods currently are:
- list/retrieve
   - ownership
- update read

### APIs

There are numerous API endpoints available for different front ends to interact with notifications.

As of this writing the available endpoints are:
- /notifications/emails/
  - GET     - list
  - GET     - retrieve (@param id)
- /notifications/basic/
  - GET     - list
  - GET     - retrieve (@param id)
  - POST    - create (@param message)
  - PATCH   - partial_update (@param read)
- /notifications/push/
  - GET     - list
  - GET     - retrieve (@param id)
  - POST    - create (@param message)





