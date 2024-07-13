from ..base import BaseModelTestCase
from ....models.push import NotificationPush

"""
# ========================================================================= #
# TEST PUSH NOTIFICATION ================================================== #
# ========================================================================= #
"""


class TestPushNotification(BaseModelTestCase):
    model = NotificationPush

    def setUp(self):
        super(TestPushNotification, self).setUp()

    # =================================================================== #
    # BASIC TESTS ======================================================= #
    # =================================================================== #

    def test_str(self):
        notification = self.model.objects.create(
            recipients=self.base_email, sender=self.base_email
        )
        self.assertEqual(str(notification), f"Notification Push: {self.base_email}")

    def test_with_message(self):
        message = "this is a test message"
        notification = self.model.objects.create(
            recipients=self.base_email, sender=self.base_email, message=message
        )
        self.assertEqual(notification.message, message)

    def test_recipients(self):
        recipients = ["user1@example.com", "user2@example.com"]
        notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email, message="Test Message"
        )
        self.assertEqual(notification.recipients, ",".join(recipients))

    def test_sender(self):
        sender = "sender@example.com"
        notification = self.model.objects.create(
            recipients=self.base_email, sender=sender, message="Test Message"
        )
        self.assertEqual(notification.sender, sender)
