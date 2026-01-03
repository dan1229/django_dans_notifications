#!/usr/bin/env python
"""
Test script to preview the new email templates
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_dans_notifications.test.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.template.loader import render_to_string


def test_templates():
    """Test and save rendered email templates as HTML files"""

    # Test data
    context = {
        'team_name': 'Awesome Company',
        'recipient_name': 'John Doe',
        'subject': 'Welcome to Our Service',
        'support_email': 'support@example.com',
        'company_address': '123 Business St, Suite 100, City, ST 12345',
        'privacy_url': 'https://example.com/privacy',
        'terms_url': 'https://example.com/terms',
        'unsubscribe_url': 'https://example.com/unsubscribe',

        # Contact form specific
        'name': 'Jane Smith',
        'email': 'jane@example.com',
        'phone': '+1 (555) 123-4567',
        'message': 'Hello,\n\nI am interested in learning more about your services. I have a few questions:\n\n1. What are your pricing plans?\n2. Do you offer custom solutions?\n3. How can I schedule a demo?\n\nPlease get back to me at your earliest convenience.\n\nBest regards,\nJane',

        # Password reset specific
        'reset_url': 'https://example.com/reset-password?token=abc123def456',
        'expiry_hours': 24,
    }

    templates = [
        ('django-dans-emails/base_improved.html', 'test_base_improved.html'),
        ('django-dans-emails/contact_improved.html', 'test_contact_improved.html'),
        ('django-dans-emails/password_reset_improved.html', 'test_password_reset_improved.html'),
    ]

    for template_path, output_file in templates:
        try:
            html_content = render_to_string(template_path, context)

            # Save to file
            with open(output_file, 'w') as f:
                f.write(html_content)

            print(f"✅ Successfully rendered {template_path} -> {output_file}")

        except Exception as e:
            print(f"❌ Error rendering {template_path}: {e}")


if __name__ == '__main__':
    test_templates()
    print("\n📧 Email templates have been generated. Open the HTML files in a browser to preview them.")