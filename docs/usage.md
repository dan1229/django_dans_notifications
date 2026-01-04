# Usage Guide

Quick examples for using Django Dans Notifications.

## Sending Emails

### Basic Example

```python
from django_dans_notifications.models.notifications import NotificationEmail

notification = NotificationEmail.objects.send_email(
    subject="Welcome to Our App",
    template="django-dans-emails/default.html",
    sender="noreply@example.com",
    recipients=["user@example.com"],
    context={"team_name": "My Team"}
)
```

### With Multiple Recipients

```python
notification = NotificationEmail.objects.send_email(
    subject="Team Update",
    template="django-dans-emails/default.html",
    sender="team@example.com",
    recipients=["user1@example.com", "user2@example.com"],
    context={"team_name": "Dev Team"}
)
```

### With File Attachment

```python
from django.core.files.base import ContentFile

file_content = ContentFile(b"CSV data here", name="report.csv")

notification = NotificationEmail.objects.send_email(
    subject="Monthly Report",
    template="django-dans-emails/empty.html",
    sender="reports@example.com",
    recipients=["manager@example.com"],
    context={"message": "Report attached."},
    file_attachment=file_content
)
```

### Using Custom Templates

```python
# Place template in templates/emails/welcome.html
notification = NotificationEmail.objects.send_email(
    subject="Welcome!",
    template="emails/welcome.html",
    sender="hello@example.com",
    recipients=["newuser@example.com"],
    context={
        "username": "johndoe",
        "activation_link": "https://example.com/activate/123"
    }
)
```

## Basic Notifications

For in-app notification systems:

```python
from django_dans_notifications.models.notifications import NotificationBasic

# Create notification
notification = NotificationBasic.objects.create(
    message="Your profile has been updated",
    sender="system@example.com",
    recipients="user@example.com"
)

# Mark as read
notification.read = True
notification.save()

# Query unread notifications
unread = NotificationBasic.objects.filter(
    recipients__contains="user@example.com",
    read=False
)
```

## Push Notifications

```python
from django_dans_notifications.models.notifications import NotificationPush

notification = NotificationPush.objects.create(
    message="New message from John",
    sender="john@example.com",
    recipients="user@example.com"
)
```

## Using NotificationManager

The `NotificationManager` utility provides convenient methods:

```python
from django_dans_notifications.utils import NotificationManager

manager = NotificationManager()

# Get notifications by type
email_notifications = manager.get_notifications_email(user=request.user)
basic_notifications = manager.get_notifications_basic(user=request.user)
push_notifications = manager.get_notifications_push(user=request.user)

# Mark basic notification as read
manager.mark_notification_basic_read(notification_id=123)
```

## Configuration Tips

### Testing Mode
```python
# settings.py
IN_TEST = True  # Prevents actual email sending during tests
```

### Debug Email Issues
```python
# settings.py
EMAIL_SYNC_MODE = True  # Disable async for debugging
```

### Performance Tuning
```python
# settings.py
EMAIL_MAX_WORKERS = 10  # Increase for high volume
EMAIL_MAX_RETRIES = 5   # More retries for unreliable networks
```

For more details, see:
- [Model Documentation](models.md) for field details
- [Email Templates](email-templates.md) for template customization
- [API Documentation](apis.md) for REST endpoints