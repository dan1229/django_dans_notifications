# Email Templates

Django Dans Notifications uses Django's template engine for HTML emails. Templates are automatically registered as `EmailTemplate` objects viewable in the Django admin.

## Built-in Templates

All templates are responsive and tested across major email clients.

### 1. default.html
General-purpose template.

| Variable | Required | Description |
|----------|----------|-------------|
| `team_name` | No | Organization name |
| `message` | No | Main content |

### 2. contact.html
For contact form submissions.

| Variable | Required | Description |
|----------|----------|-------------|
| `name` | Yes | Contact person's name |
| `email` | Yes | Contact person's email |
| `message` | Yes | Contact message |
| `team_name` | No | Organization name |

### 3. empty.html
Minimal template for simple messages.

| Variable | Required | Description |
|----------|----------|-------------|
| `message` | Yes | Email content |
| `team_name` | No | Organization name |

### 4. password_reset.html
For password reset emails.

| Variable | Required | Description |
|----------|----------|-------------|
| `password_reset_url` | Yes | Reset URL |
| `team_name` | No | Organization name |
| `expiry_time` | No | Link expiration time |

## Creating Custom Templates

### Setup

1. Ensure templates directory is configured:
```python
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
    },
]
```

2. Create your template:
```
project/
├── templates/
│   ├── emails/
│   │   └── welcome.html
```

### Basic Template Structure

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* Inline CSS for email compatibility */
        body { font-family: Arial, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello {{ username }}!</h1>
        <p>{{ message }}</p>
        {% if team_name %}
        <p>Best regards,<br>{{ team_name }}</p>
        {% endif %}
    </div>
</body>
</html>
```

### Using Custom Templates

```python
NotificationEmail.objects.send_email(
    subject="Welcome!",
    template="emails/welcome.html",  # Your template path
    sender="hello@example.com",
    recipients=["user@example.com"],
    context={
        "username": "John",
        "message": "Welcome to our platform!"
    }
)
```

## Email Best Practices

### Compatibility
- Use inline CSS (not external stylesheets)
- Use table layouts for complex designs
- Test with major email clients

### Responsive Design
```css
@media only screen and (max-width: 600px) {
    .container { width: 100% !important; }
}
```

### Accessibility
- Use semantic HTML (`<h1>`, `<p>`, etc.)
- Add alt text to images
- Ensure sufficient color contrast

## Template Discovery

Templates are automatically discovered when:
- Placed in `templates/emails/` directory
- First used with `send_email()`
- Django server is restarted

## Admin Interface

View and manage templates in Django admin under "Email Templates".

## Troubleshooting

### Template Not Found
```python
from django.template.loader import get_template
try:
    template = get_template("emails/custom.html")
except TemplateDoesNotExist:
    print("Check template path and TEMPLATES setting")
```

### Context Variables Not Rendering
Check the stored context in the notification:
```python
print(notification.context)  # View JSON in database
```

### CSS Issues
- Always inline CSS for emails
- Use style tags only for media queries
- Test with tools like Litmus or Email on Acid