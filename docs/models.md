# Model Documentation

## Base Model: `NotificationBase`

All notification models inherit from this base class.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `recipients` | CharField | Yes | Comma-separated list of recipient emails |
| `sender` | EmailField | Yes | Sender email address |
| `datetime_sent` | DateTimeField | Auto | Timestamp (auto-set on creation) |
| `sent_successfully` | BooleanField | No | Whether successfully processed (default: False) |

## `NotificationEmail`

For email notifications with template support.

### Additional Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `subject` | CharField | Yes | Email subject (max 255 chars) |
| `content` | TextField | No | Email body (HTML supported) |
| `template_used` | CharField | No | Template file path |
| `context` | JSONField | No | Template context variables |
| `file_attachment` | FileField | No | File attachment |

### Manager Method

`send_email(subject, template, sender, recipients, context={}, file_attachment=None)`
- Sends email asynchronously with retry logic
- Auto-creates EmailTemplate objects
- Returns NotificationEmail instance

## `NotificationBasic`

For in-app notifications.

### Additional Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | TextField | Yes | Notification message |
| `read` | BooleanField | No | Read status (default: False) |
| `read_datetime` | DateTimeField | No | When marked as read |

## `NotificationPush`

For push notifications.

### Additional Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | TextField | Yes | Push notification message |
| `data` | JSONField | No | Additional payload |
| `device_tokens` | TextField | No | Comma-separated device tokens |
| `platform` | CharField | No | Target platform (iOS/Android/Web) |

## EmailTemplate Model

Auto-created when templates are used.

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField | Template file name |
| `subject` | CharField | Default subject |
| `content` | TextField | Template HTML content |
| `template_path` | CharField | File system path |

## Database Optimization

### Recommended Indexes

```python
class Meta:
    indexes = [
        models.Index(fields=['recipients', '-datetime_sent']),
        models.Index(fields=['sent_successfully']),
        models.Index(fields=['read']),  # For NotificationBasic
    ]
```

### Efficient Queries

```python
# Recent unread notifications
NotificationBasic.objects.filter(
    recipients__contains=user_email,
    read=False,
    datetime_sent__gte=timezone.now() - timedelta(days=7)
).order_by('-datetime_sent')[:10]
```

## Admin Interface

All models are registered with Django Admin for easy management.

See [Usage Guide](usage.md) for code examples.