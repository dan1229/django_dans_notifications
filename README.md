# DJANGO DANS NOTIFICATION

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



## Packaging

To build run:

```bash
python setup.py sdist
python setup.py bdist_wheel
```

To release run:

```bash
python3 -m twine upload --repository testpypi dist/*
```

This expects you to have the proper credentials in your `$HOME/.pypirc` file