from .base import BaseSerializer
from ..models.basic import NotificationBasic

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
