from django.db.models import Q

from notifications.models import NotificationEmail, NotificationBasic, NotificationPush

"""
============================================================================================ #
NOTIFICATION MANAGER ======================================================================= #
============================================================================================ #
"""


#
# Generic manager for notification models
#
# Not sure if this will be useful or necessary, can be used to enforce ownership
# on list/retrieval function.
#
# Ideally all CRUD actions on notifications would be done through this to make it a
# bit simpler but that would be a lot of parameter drilling at the moment.
#
class NotificationManager:
    @staticmethod
    def query_ownership(user_email):
        return Q(sender__contains=user_email) | Q(recipients__contains=user_email)

    #
    # RETRIEVE
    #
    def get_notifications_email(self, user_email):
        return NotificationEmail.objects.filter(self.query_ownership(user_email))

    def get_notifications_basic(self, user_email):
        return NotificationBasic.objects.filter(self.query_ownership(user_email))

    def get_notifications_push(self, user_email):
        return NotificationPush.objects.filter(self.query_ownership(user_email))

    def get_notifications_all(self, user_email):
        emails = self.get_notifications_email(user_email=user_email)
        basic = self.get_notifications_basic(user_email=user_email)
        push = self.get_notifications_push(user_email=user_email)

    #
    # UPDATE
    #
    @staticmethod
    def mark_notification_read(notification_basic, read=True):
        notification_basic.read = read
        notification_basic.save()
