from ..base import BaseModelTestCase
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
            path="django-dans-emails/template.html",
        )
        super(TestEmailNotification, self).setUp()

    # =================================================================== #
    # BASIC TESTS ======================================================= #
    # =================================================================== #

    def test_str(self):
        notification = self.model.objects.create(
            template=self.email_template,
            recipients=self.base_email,
            sender=self.base_email,
        )
        self.assertEqual(
            str(notification),
            f"Notification Email: {self.base_email} -> {self.base_email}",
        )

    def test_with_subject(self):
        subject = "this is a test subject"
        notification = self.model.objects.create(
            template=self.email_template,
            recipients=self.base_email,
            sender=self.base_email,
            subject=subject,
        )
        self.assertEqual(notification.subject, subject)

    def test_with_context(self):
        context = {"user": "213542465346"}
        notification = self.model.objects.create(
            template=self.email_template,
            recipients=self.base_email,
            sender=self.base_email,
            context=context,
        )
        self.assertEqual(notification.context, context)

    def test_with_no_template(self):
        notification = self.model.objects.create(
            recipients=self.base_email,
            sender=self.base_email,
            subject="No Template Test",
        )
        self.assertEqual(
            notification.template,
            NotificationEmailTemplate.objects.get(
                path="django-dans-emails/default.html"
            ),
        )

    def test_with_recipients(self):
        recipients = ["user1@example.com", "user2@example.com"]
        notification = self.model.objects.create(
            template=self.email_template, recipients=recipients, sender=self.base_email
        )
        self.assertEqual(notification.recipients, ",".join(recipients))
