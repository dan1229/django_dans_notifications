"""
Django Dans Notifications Settings

This module provides configuration settings for email templates and notifications.
Users can customize these settings in their Django settings file.
"""

from django.conf import settings


class EmailTemplateSettings:
    """
    Email template configuration settings.

    Users can override these in their Django settings using DANS_NOTIFICATIONS dict:

    DANS_NOTIFICATIONS = {
        'EMAIL_TEMPLATE_BASE': 'django-dans-emails/base_improved.html',
        'EMAIL_TEMPLATE_STYLE': 'improved',  # 'classic' or 'improved'
        'EMAIL_BRANDING': {
            'team_name': 'Your Company',
            'logo_url': 'https://example.com/logo.png',
            'primary_color': '#4F46E5',
            'primary_color_hover': '#4338CA',
            'support_email': 'support@example.com',
            'company_address': '123 Main St, City, ST 12345',
            'privacy_url': 'https://example.com/privacy',
            'terms_url': 'https://example.com/terms',
            'social_links': [
                {'name': 'Twitter', 'url': 'https://twitter.com/yourcompany', 'icon': 'url-to-icon'},
                {'name': 'LinkedIn', 'url': 'https://linkedin.com/company/yourcompany', 'icon': 'url-to-icon'},
            ]
        }
    }
    """

    def __init__(self):
        self._settings = getattr(settings, 'DANS_NOTIFICATIONS', {})

    @property
    def email_template_base(self):
        """Get the base email template path"""
        default = 'django-dans-emails/base.html'
        style = self._settings.get('EMAIL_TEMPLATE_STYLE', 'classic')

        if style == 'improved':
            default = 'django-dans-emails/base_improved.html'

        return self._settings.get('EMAIL_TEMPLATE_BASE', default)

    @property
    def email_template_style(self):
        """Get the email template style (classic or modern)"""
        return self._settings.get('EMAIL_TEMPLATE_STYLE', 'classic')

    @property
    def email_branding(self):
        """Get email branding configuration"""
        return self._settings.get('EMAIL_BRANDING', {})

    @property
    def team_name(self):
        """Get team/company name"""
        branding = self.email_branding
        return branding.get('team_name', getattr(settings, 'SITE_NAME', None))

    @property
    def logo_url(self):
        """Get logo URL"""
        return self.email_branding.get('logo_url')

    @property
    def primary_color(self):
        """Get primary brand color"""
        return self.email_branding.get('primary_color', '#4F46E5')

    @property
    def support_email(self):
        """Get support email address"""
        branding = self.email_branding
        return branding.get('support_email', getattr(settings, 'DEFAULT_FROM_EMAIL', None))

    def get_template_for_type(self, template_type):
        """
        Get the appropriate template path for a given type

        Args:
            template_type: Type of template (e.g., 'contact', 'password_reset', 'notification')

        Returns:
            Template path string
        """
        style = self.email_template_style

        template_map = {
            'classic': {
                'base': 'django-dans-emails/base.html',
                'contact': 'django-dans-emails/contact.html',
                'password_reset': 'django-dans-emails/password_reset_request.html',
                'default': 'django-dans-emails/default.html',
            },
            'improved': {
                'base': 'django-dans-emails/base_improved.html',
                'contact': 'django-dans-emails/contact_improved.html',
                'password_reset': 'django-dans-emails/password_reset_improved.html',
                'default': 'django-dans-emails/base_improved.html',
            }
        }

        templates = template_map.get(style, template_map['classic'])
        return templates.get(template_type, templates['default'])

    def get_context_defaults(self):
        """
        Get default context variables for email templates

        Returns:
            Dictionary of default context variables
        """
        branding = self.email_branding

        return {
            'team_name': self.team_name,
            'logo_url': self.logo_url,
            'primary_color': self.primary_color,
            'primary_color_hover': branding.get('primary_color_hover', '#4338CA'),
            'support_email': self.support_email,
            'company_address': branding.get('company_address'),
            'privacy_url': branding.get('privacy_url'),
            'terms_url': branding.get('terms_url'),
            'unsubscribe_url': branding.get('unsubscribe_url'),
            'social_links': branding.get('social_links', []),
            'copyright_text': branding.get('copyright_text'),
            'signature_greeting': branding.get('signature_greeting', 'Best regards,'),
        }


# Singleton instance
email_settings = EmailTemplateSettings()