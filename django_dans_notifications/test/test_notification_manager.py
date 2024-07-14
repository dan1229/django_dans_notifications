from .model_tests.base import BaseModelTestCase
from ..models.notifications import (
    NotificationEmail,
    NotificationEmailTemplate,
    NotificationBasic,
    NotificationPush,
)
from ..notification_manager import NotificationManager

"""
# ========================================================================= #
# TEST NOTIFICATION MANAGER =============================================== #
# ========================================================================= #
"""


class TestNotificationManager(BaseModelTestCase):
    def setUp(self) -> None:
        super(TestNotificationManager, self).setUp()
        self.manager = NotificationManager()

        # Set up test data
        self.email_template = NotificationEmailTemplate.objects.create(
            nickname="template1", path="django-dans-emails/template.html"
        )

        self.notification_email = NotificationEmail.objects.create(
            template=self.email_template,
            recipients=self.base_email,
            sender=self.base_email,
            subject="Email Subject",
        )

        self.notification_basic = NotificationBasic.objects.create(
            recipients=self.base_email, sender=self.base_email, message="Basic Message"
        )

        self.notification_push = NotificationPush.objects.create(
            recipients=self.base_email, sender=self.base_email, message="Push Message"
        )

    # =================================================================== #
    # RETRIEVE TESTS ==================================================== #
    # =================================================================== #

    def test_get_notifications_email(self) -> None:
        notifications = self.manager.get_notifications_email(self.base_email)
        self.assertIn(self.notification_email, notifications)

    def test_get_notifications_basic(self) -> None:
        notifications = self.manager.get_notifications_basic(self.base_email)
        self.assertIn(self.notification_basic, notifications)

    def test_get_notifications_push(self) -> None:
        notifications = self.manager.get_notifications_push(self.base_email)
        self.assertIn(self.notification_push, notifications)

    def test_get_notifications_all(self) -> None:
        notifications = self.manager.get_notifications_all(self.base_email)
        self.assertIn(self.notification_email, notifications["emails"])
        self.assertIn(self.notification_basic, notifications["basic"])
        self.assertIn(self.notification_push, notifications["push"])

    # =================================================================== #
    # UPDATE TESTS ====================================================== #
    # =================================================================== #

    def test_mark_notification_basic_read(self) -> None:
        self.manager.mark_notification_basic_read(self.notification_basic, read=True)
        self.notification_basic.refresh_from_db()
        self.assertTrue(self.notification_basic.read)

    def test_mark_notification_basic_unread(self) -> None:
        self.notification_basic.read = True
        self.notification_basic.save()  # type: ignore[no-untyped-call]
        self.manager.mark_notification_basic_read(self.notification_basic, read=False)
        self.notification_basic.refresh_from_db()
        self.assertFalse(self.notification_basic.read)
