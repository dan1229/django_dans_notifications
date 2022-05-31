from ..base import (
    BaseModelTestCase,
)
from ....models.email import NotificationEmail, NotificationEmailTemplate

"""
# ========================================================================= #
# TEST EMAIL NOTIFICATION ================================================= #
# ========================================================================= #
"""


class TestEmailNotification(BaseModelTestCase):
    model = NotificationEmail

    def setUp(self):
        self.email_template_nickname = "template1"
        self.email_template = NotificationEmailTemplate.objects.create(
            nickname=self.email_template_nickname,
        )
        super(TestEmailNotification, self).setUp()

    # =================================================================== #
    # BASIC TESTS ======================================================= #
    # =================================================================== #

    def test_str(self):
        self.notification = self.model.objects.create(
            template=self.email_template,
            recipients=self.base_email,
            sender=self.base_email,
        )
        self.assertNotEqual(str(self.notification), None)

    def test_with_subject(self):
        subject = "this is a test subject"
        self.notification = self.model.objects.create(
            recipients=self.base_email, sender=self.base_email, subject=subject
        )

        self.assertEqual(self.notification.subject, subject)

    def test_with_context(self):
        context = {"user": "213542465346"}
        self.notification = self.model.objects.create(
            recipients=self.base_email, sender=self.base_email, context=context
        )

        self.assertEqual(self.notification.context, context)
