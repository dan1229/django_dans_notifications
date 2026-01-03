# Email Templates Documentation

## Available Templates

### Classic Templates (Original)
- `base.html` - Simple base template
- `contact.html` - Basic contact form email
- `password_reset_request.html` - Basic password reset email
- `default.html` - Default template
- `template.html` - Empty template with content block
- `empty.html` - Minimal template

### Improved Templates (Professional & Modern)
- `base_improved.html` - Enhanced base template with modern styling
- `contact_improved.html` - Professional contact form email
- `password_reset_improved.html` - Enhanced password reset email

## Using the Improved Templates

### Quick Setup

Add to your Django settings:

```python
DANS_NOTIFICATIONS = {
    'EMAIL_TEMPLATE_STYLE': 'improved',  # Use improved templates
    'EMAIL_BRANDING': {
        'team_name': 'Your Company Name',
        'logo_url': 'https://example.com/logo.png',
        'primary_color': '#4F46E5',
        'support_email': 'support@yourcompany.com',
        'company_address': '123 Main St, City, ST 12345',
        'privacy_url': 'https://yourcompany.com/privacy',
        'terms_url': 'https://yourcompany.com/terms',
    }
}
```

### Using Email Utilities

```python
from django_dans_notifications.email_utils import send_contact_email, send_password_reset_email

# Send a contact form email
send_contact_email(
    name="John Doe",
    email="john@example.com",
    message="I'm interested in your services...",
    subject="Inquiry",
    phone="+1-555-0123"
)

# Send a password reset email
send_password_reset_email(
    user_email="user@example.com",
    reset_url="https://example.com/reset?token=abc123",
    user_name="Jane Doe",
    expiry_hours=24
)
```

### Template Variables

#### Base Template (`base_improved.html`)
- `team_name` - Company/team name
- `logo_url` - Logo image URL
- `recipient_name` - Recipient's name
- `primary_color` - Main brand color (default: #4F46E5)
- `primary_color_hover` - Hover color for buttons
- `support_email` - Support email address
- `company_address` - Physical address
- `privacy_url` - Privacy policy link
- `terms_url` - Terms of service link
- `unsubscribe_url` - Unsubscribe link
- `social_links` - List of social media links
- `copyright_text` - Custom copyright text
- `signature_greeting` - Email signature greeting

#### Contact Template (`contact_improved.html`)
All base variables plus:
- `name` - Sender's name
- `email` - Sender's email
- `message` - Message content
- `phone` - Phone number (optional)
- `subject` - Message subject (optional)
- `admin_url` - Link to admin panel (optional)
- `ip_address` - Sender's IP address (optional)

#### Password Reset Template (`password_reset_improved.html`)
All base variables plus:
- `reset_url` - Password reset link
- `expiry_hours` - Link expiration time

## Features

### Improved Templates Include:
- ✅ Responsive design (mobile-friendly)
- ✅ Professional modern styling
- ✅ Customizable brand colors
- ✅ Better typography and spacing
- ✅ Support for logos and social links
- ✅ Preheader text support
- ✅ Structured footer with legal links
- ✅ Cross-client compatibility
- ✅ Dark mode considerations
- ✅ Accessible HTML structure

## Testing Templates

Run the test script to preview templates:

```bash
python test_email_templates.py
```

This generates HTML files you can open in a browser to preview.