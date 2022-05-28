from api.serializers.base import BaseSerializer
from notifications.models.push import NotificationPush

"""
============================================================================================ #
PUSH SERIALIZERS =========================================================================== #
============================================================================================ #
"""


#
# NOTIFICATION PUSH ========================== #
#
class NotificationPushSerializer(BaseSerializer):
    class Meta:
        model = NotificationPush
        fields = (
            "id",
            "message",
            "datetime_sent",
            "sent_successfully",
            "sender",
            "recipients",
        )
        read_only_fields = (
            "id",
            "datetime_sent",
            "sent_successfully",
            "sender",
        )
