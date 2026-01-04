from django_dans_api_toolkit.serializers.base import BaseSerializer
from rest_framework import serializers

from .models.notifications import (
    NotificationPush,
    NotificationEmailTemplate,
    NotificationEmail,
    NotificationBasic,
)


#
# NOTIFICATION BASIC ========================== #
#
class NotificationBasicSerializer(BaseSerializer):
    """
    Serializer for basic text notifications.

    Basic notifications are simple text messages that can be marked as read/unread.
    """

    class Meta:
        model = NotificationBasic
        fields = (
            "id",
            "message",
            "read",
            "datetime_created",
            "datetime_sent",
            "sent_successfully",
            "sender",
            "recipients",
        )
        read_only_fields = (
            "id",
            "datetime_created",
        )
        extra_kwargs = {
            'message': {
                'help_text': 'The notification message content'
            },
            'read': {
                'help_text': 'Whether the notification has been marked as read'
            },
            'datetime_created': {
                'help_text': 'Timestamp when the notification was created'
            },
            'datetime_sent': {
                'help_text': 'Timestamp when the notification was sent'
            },
            'sent_successfully': {
                'help_text': 'Whether the notification was sent successfully'
            },
            'sender': {
                'help_text': 'Email address of the notification sender'
            },
            'recipients': {
                'help_text': 'List of recipient emails or user IDs'
            }
        }


#
# NOTIFICATION EMAIL TEMPLATE ========================== #
#
class NotificationEmailTemplateSerializer(BaseSerializer):
    """
    Serializer for email notification templates.

    Email templates define the HTML structure and styling for email notifications.
    """

    class Meta:
        model = NotificationEmailTemplate
        fields = (
            "id",
            "path",
            "nickname",
        )
        extra_kwargs = {
            'path': {
                'help_text': 'File path to the email template'
            },
            'nickname': {
                'help_text': 'Human-readable name for the template'
            }
        }


#
# NOTIFICATION EMAIL ========================== #
#
class NotificationEmailSerializer(BaseSerializer):
    """
    Serializer for email notifications.

    Email notifications use templates and context data to generate HTML content.
    """
    template_ref = NotificationEmailTemplateSerializer(
        source="template", required=False, help_text="Template details (read-only)"
    )
    content = serializers.SerializerMethodField(
        help_text="Rendered HTML content of the email"
    )

    class Meta:
        model = NotificationEmail
        fields = (
            "id",
            "template",
            "template_ref",
            "subject",
            "context",
            "datetime_created",
            "datetime_sent",
            "sent_successfully",
            "sender",
            "recipients",
            "content",
        )
        read_only_fields = (
            "id",
            "template_ref",
            "datetime_created",
        )
        extra_kwargs = {
            'template': {
                'help_text': 'ID of the email template to use'
            },
            'subject': {
                'help_text': 'Email subject line'
            },
            'context': {
                'help_text': 'JSON context data for template rendering'
            },
            'datetime_created': {
                'help_text': 'Timestamp when the notification was created'
            },
            'datetime_sent': {
                'help_text': 'Timestamp when the notification was sent'
            },
            'sent_successfully': {
                'help_text': 'Whether the email was sent successfully'
            },
            'sender': {
                'help_text': 'Email address of the sender'
            },
            'recipients': {
                'help_text': 'List of recipient emails or user IDs'
            }
        }

    @staticmethod
    def get_content(obj: NotificationEmail) -> str:
        """Render the email template with context data to generate HTML content."""
        return str(obj.template.html_to_str(obj.context))


#
# NOTIFICATION PUSH ========================== #
#
class NotificationPushSerializer(BaseSerializer):
    """
    Serializer for push notifications.

    Push notifications are sent to mobile devices or web browsers.
    """

    class Meta:
        model = NotificationPush
        fields = (
            "id",
            "message",
            "datetime_created",
            "datetime_sent",
            "sent_successfully",
            "sender",
            "recipients",
        )
        read_only_fields = (
            "id",
            "datetime_created",
        )
        extra_kwargs = {
            'message': {
                'help_text': 'The push notification message content'
            },
            'datetime_created': {
                'help_text': 'Timestamp when the notification was created'
            },
            'datetime_sent': {
                'help_text': 'Timestamp when the notification was sent'
            },
            'sent_successfully': {
                'help_text': 'Whether the push notification was sent successfully'
            },
            'sender': {
                'help_text': 'Email address of the notification sender'
            },
            'recipients': {
                'help_text': 'List of recipient emails or user IDs'
            }
        }
