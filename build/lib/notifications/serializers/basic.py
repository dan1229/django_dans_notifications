from notifications.models.basic import NotificationBasic
from .base import BaseSerializer

"""
============================================================================================ #
BASIC SERIALIZERS ========================================================================== #
============================================================================================ #
"""


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
            "datetime_sent",
            "sent_successfully",
            "sender",
            "recipients",
        )
