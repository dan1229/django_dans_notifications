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

## Quick Start

```bash
pip install django-dans-notifications
```

See the [Getting Started Guide](https://github.com/dan1229/django_dans_notifications/tree/main/docs/getting-started.md) for detailed installation and configuration instructions.

### Requirements

- Python 3.8 or higher
- Django 3.1 or higher
- Django Rest Framework (with authentication configured)

### Basic Usage

```python
from django_dans_notifications.models.notifications import NotificationEmail

# Send an email notification
notification = NotificationEmail.objects.send_email(
    subject="Welcome",
    template="django-dans-emails/default.html",
    sender="noreply@example.com",
    recipients=["user@example.com"],
    context={"team_name": "My Team"}
)
```

See the [Usage Guide](https://github.com/dan1229/django_dans_notifications/tree/main/docs/usage.md) for more examples and advanced usage.

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

## Documentation

- **[Getting Started](https://github.com/dan1229/django_dans_notifications/tree/main/docs/getting-started.md)** - Installation and configuration
- **[Usage Guide](https://github.com/dan1229/django_dans_notifications/tree/main/docs/usage.md)** - How to send notifications and use the app
- **[API Documentation](https://github.com/dan1229/django_dans_notifications/tree/main/docs/apis.md)** - REST API endpoints reference
- **[Model Documentation](https://github.com/dan1229/django_dans_notifications/tree/main/docs/models.md)** - Detailed model information
- **[Email Templates](https://github.com/dan1229/django_dans_notifications/tree/main/docs/email-templates.md)** - Template system and customization

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/dan1229/django_dans_notifications).

-------------------------------------------------------

##### [https://danielnazarian.com](https://danielnazarian.com)

##### Copyright 2024 © Daniel Nazarian.

