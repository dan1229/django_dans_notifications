from django.db import models

from .base import NotificationBase

"""
# ==================================================================================== #
# NOTIFICATION PUSH ================================================================== #
# ==================================================================================== #
"""


#
# NOTIFICATION PUSH ================== #
#


class NotificationPush(NotificationBase):
    message = models.CharField(max_length=300, null=False, blank=False)

    def __str__(self):
        return f"Notification Push: {self.recipients}"
