from django.db import models

from .base import NotificationBase

"""
# ==================================================================================== #
# NOTIFICATION BASIC ================================================================= #
# ==================================================================================== #
"""


#
# NOTIFICATION BASIC ==================== #
#
class NotificationBasic(NotificationBase):
    read = models.BooleanField(default=False, null=False, blank=False)
    message = models.CharField(max_length=600, null=False, blank=False)

    def __str__(self):
        return f"Basic Notification: {self.recipients}"
