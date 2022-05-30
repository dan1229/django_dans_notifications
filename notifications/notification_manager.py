from django.db.models import Q

from .models import NotificationEmail, NotificationBasic, NotificationPush

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
        """
        Get all the EMAIL notifications associated with this user
        :param str user_email: user email to search

        :returns: NotificationEmail queryset
        """
        return NotificationEmail.objects.filter(self.query_ownership(user_email))

    def get_notifications_basic(self, user_email):
        """
        Get all the BASIC notifications associated with this user
        :param str user_email: user email to search

        :returns: NotificationBasic queryset
        """
        return NotificationBasic.objects.filter(self.query_ownership(user_email))

    def get_notifications_push(self, user_email):
        """
        Get all the PUSH notifications associated with this user
        :param str user_email: user email to search

        :returns: NotificationPush queryset
        """
        return NotificationPush.objects.filter(self.query_ownership(user_email))

    def get_notifications_all(self, user_email):
        """
        Get all the notifications associated with this user
        :param str user_email: user email to search

        :returns: dict containing all this users different types of notifications
        :rtype: {'emails': emails, 'basic': basic, 'push': push}
        """
        emails = self.get_notifications_email(user_email=user_email)
        basic = self.get_notifications_basic(user_email=user_email)
        push = self.get_notifications_push(user_email=user_email)
        return {"emails": emails, "basic": basic, "push": push}

    #
    # UPDATE
    #
    @staticmethod
    def mark_notification_basic_read(notification_basic, read=True):
        """
        Mark a NotificationBasic as read
        :param NotificationBasic notification_basic: notification basic to update
        :param bool read: mark read or not
        """
        notification_basic.read = read
        notification_basic.save()
