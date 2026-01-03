"""
Email utility functions for django_dans_notifications

Provides helper functions to send emails using the configured templates.
"""

from typing import Dict, List, Optional, Union
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings as django_settings

from .settings import email_settings


def prepare_email_context(context: Optional[Dict] = None) -> Dict:
    """
    Prepare email context with default branding values

    Args:
        context: Custom context variables to include

    Returns:
        Dictionary with merged context
    """
    base_context = email_settings.get_context_defaults()

    if context:
        base_context.update(context)

    return base_context


def send_templated_email(
    template_type: str,
    recipient_email: Union[str, List[str]],
    subject: str,
    context: Optional[Dict] = None,
    from_email: Optional[str] = None,
    reply_to: Optional[List[str]] = None,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    attachments: Optional[List] = None,
    custom_template: Optional[str] = None,
) -> bool:
    """
    Send an email using the configured template system

    Args:
        template_type: Type of template ('contact', 'password_reset', etc.)
        recipient_email: Email address(es) to send to
        subject: Email subject line
        context: Template context variables
        from_email: From email address (defaults to DEFAULT_FROM_EMAIL)
        reply_to: Reply-to email addresses
        cc: CC recipients
        bcc: BCC recipients
        attachments: List of attachments
        custom_template: Override template path

    Returns:
        True if email was sent successfully, False otherwise
    """
    try:
        # Get template path
        if custom_template:
            template_path = custom_template
        else:
            template_path = email_settings.get_template_for_type(template_type)

        # Prepare context
        email_context = prepare_email_context(context)
        email_context['subject'] = subject

        # Render HTML content
        html_content = render_to_string(template_path, email_context)

        # Generate plain text version
        text_content = strip_tags(html_content)

        # Prepare recipient list
        if isinstance(recipient_email, str):
            recipient_list = [recipient_email]
        else:
            recipient_list = recipient_email

        # Get from email
        if not from_email:
            from_email = getattr(django_settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')

        # Create email message
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=recipient_list,
            reply_to=reply_to,
            cc=cc,
            bcc=bcc,
        )

        # Attach HTML version
        email.attach_alternative(html_content, "text/html")

        # Add attachments if any
        if attachments:
            for attachment in attachments:
                if isinstance(attachment, tuple):
                    email.attach(*attachment)
                else:
                    email.attach_file(attachment)

        # Send email
        email.send(fail_silently=False)
        return True

    except Exception as e:
        # Log the error (you might want to use proper logging here)
        print(f"Error sending email: {e}")
        return False


def send_contact_email(
    name: str,
    email: str,
    message: str,
    subject: Optional[str] = None,
    phone: Optional[str] = None,
    recipient_email: Optional[str] = None,
    **kwargs,
) -> bool:
    """
    Send a contact form email

    Args:
        name: Sender's name
        email: Sender's email
        message: Message content
        subject: Message subject
        phone: Sender's phone number
        recipient_email: Where to send the contact form (defaults to support email)
        **kwargs: Additional context variables or email options

    Returns:
        True if email was sent successfully
    """
    if not recipient_email:
        recipient_email = email_settings.support_email or getattr(
            django_settings, 'DEFAULT_FROM_EMAIL', 'admin@example.com'
        )

    context = {
        'name': name,
        'email': email,
        'message': message,
        'phone': phone,
        'subject': subject,
    }
    context.update(kwargs)

    email_subject = f"New Contact Message from {name}"
    if subject:
        email_subject = f"Contact Form: {subject}"

    return send_templated_email(
        template_type='contact',
        recipient_email=recipient_email,
        subject=email_subject,
        context=context,
        reply_to=[email],
    )


def send_password_reset_email(
    user_email: str,
    reset_url: str,
    user_name: Optional[str] = None,
    expiry_hours: int = 24,
    **kwargs,
) -> bool:
    """
    Send a password reset email

    Args:
        user_email: User's email address
        reset_url: Password reset URL
        user_name: User's name (optional)
        expiry_hours: Link expiry time in hours
        **kwargs: Additional context variables

    Returns:
        True if email was sent successfully
    """
    context = {
        'recipient_name': user_name,
        'reset_url': reset_url,
        'expiry_hours': expiry_hours,
    }
    context.update(kwargs)

    return send_templated_email(
        template_type='password_reset',
        recipient_email=user_email,
        subject='Password Reset Request',
        context=context,
    )