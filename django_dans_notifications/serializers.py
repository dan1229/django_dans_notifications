from django_dans_api_toolkit import BaseSerializer
from rest_framework import serializers

from .models.push import NotificationPush
from .models.email import NotificationEmailTemplate, NotificationEmail
from .models.basic import NotificationBasic


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
    def get_content(obj):
        return obj.template.html_to_str(obj.context)


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
