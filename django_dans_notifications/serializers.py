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


#
# NOTIFICATION EMAIL TEMPLATE ========================== #
#
class NotificationEmailTemplateSerializer(BaseSerializer):
    class Meta:
        model = NotificationEmailTemplate
        fields = (
            "id",
            "path",
            "nickname",
        )


#
# NOTIFICATION EMAIL ========================== #
#
class NotificationEmailSerializer(BaseSerializer):
    template_ref = NotificationEmailTemplateSerializer(
        source="template", required=False
    )
    content = serializers.SerializerMethodField()

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

    @staticmethod
    def get_content(obj: NotificationEmail) -> str:
        return str(obj.template.html_to_str(obj.context))


#
# NOTIFICATION PUSH ========================== #
#
class NotificationPushSerializer(BaseSerializer):
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
