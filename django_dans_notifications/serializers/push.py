from .base import BaseSerializer
from ..models.push import NotificationPush

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
