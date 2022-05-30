from ..base import (
    BaseModelTestCase,
)
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
        self.notification = self.model.objects.create(
            recipients=self.base_email, sender=self.base_email
        )

        self.assertNotEqual(str(self.notification), None)

    def test_with_message(self):
        message = "this is a test message"
        self.notification = self.model.objects.create(
            recipients=self.base_email, sender=self.base_email, message=message
        )

        self.assertEqual(self.notification.message, message)
