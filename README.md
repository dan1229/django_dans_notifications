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

### REQUIREMENTS
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


### Email Templates
This file is intended to document and explain all the email templates in this project so you can use them properly. By default, this project will include a handful that are necessary for the app to work however as you add templates, please include them in this document.


#### default.html
Default email template. You probably will never send this, it's primarily for errors.


#### empty.html
Empty email template. Used for contact forms and messages where the 'message' or 'content' can be supplied

| Name      | Type | Required | Description                    |
|-----------|------|----------|--------------------------------|
| `message` | str  | yes      | Body message/content for email |


#### password_reset.html
Email to send on a password reset request. Should include link for user to go to, to actually reset their password.

##### Context Variables
| Name                 | Type | Required | Description           |
|----------------------|------|----------|-----------------------|
| `password_reset_url` | str  | yes      | URL to direct user to |



#### template.html
Template email. This just contains template HTML to fill in as you create new EmailTemplates. This will also probably never be explicitly sent.


