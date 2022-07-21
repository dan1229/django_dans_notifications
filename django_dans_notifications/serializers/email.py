from rest_framework import serializers

from .base import BaseSerializer
from ..models.email import NotificationEmail, NotificationEmailTemplate

"""
============================================================================================ #
EMAIL SERIALIZERS ========================================================================== #
============================================================================================ #
"""


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
