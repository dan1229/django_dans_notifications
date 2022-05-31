from ..base import BaseModelTestCase
from ....models.email import NotificationEmail

"""
# ========================================================================= #
# TEST NOTIFICATION EMAIL MANAGER ========================================= #
# ========================================================================= #
"""


class TestNotificationEmailManager(BaseModelTestCase):
    email = "test+1@example.com"
    password = "password"

    def setUp(self):
        super(TestNotificationEmailManager, self).setUp()

    # =================================================================== #
    # BASIC TESTS ======================================================= #
    # =================================================================== #

    def test_send_email_template_doesnt_exist(self):
        try:
            notification_email = NotificationEmail.objects.send_email(
                template="INVALID",
            )
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(True)

    def test_send_email_template_does_exist(self):
        template = "emails/default.html"
        notification_email = NotificationEmail.objects.send_email(
            template=template,
        )

        self.assertEqual(notification_email.template.path, template)

    def test_send_email_no_recipients(self):
        template = "emails/default.html"
        recipients = []
        notification_email = NotificationEmail.objects.send_email(
            template=template, recipients=recipients
        )

        self.assertEqual(notification_email.recipients, "")

    def test_send_email_with_one_recipients_list(self):
        email1 = "danielnazarian@outlook.com"
        template = "emails/default.html"
        recipients = [email1]
        notification_email = NotificationEmail.objects.send_email(
            template=template, recipients=recipients
        )

        self.assertEqual(notification_email.recipients, email1)

    def test_send_email_with_one_recipients_str(self):
        email1 = "danielnazarian@outlook.com"
        template = "emails/default.html"
        recipients = str([email1])
        notification_email = NotificationEmail.objects.send_email(
            template=template, recipients=recipients
        )

        self.assertEqual(notification_email.recipients, email1)

    def test_send_email_with_many_recipients_list(self):
        email1 = "danielnazarian@outlook.com"
        email2 = "danielnazarian+32523@outlook.com"
        email3 = "danielnazarian+352346@outlook.com"
        template = "emails/default.html"
        recipients = [email1, email2, email3]
        notification_email = NotificationEmail.objects.send_email(
            template=template, recipients=recipients
        )

        self.assertTrue(email1 in notification_email.recipients)
        self.assertTrue(email2 in notification_email.recipients)
        self.assertTrue(email3 in notification_email.recipients)

    def test_send_email_with_many_recipients_str(self):
        email1 = "danielnazarian@outlook.com"
        email2 = "danielnazarian+32523@outlook.com"
        email3 = "danielnazarian+352346@outlook.com"
        template = "emails/default.html"
        recipients = str([email1, email2, email3])
        notification_email = NotificationEmail.objects.send_email(
            template=template, recipients=recipients
        )

        self.assertTrue(email1 in notification_email.recipients)
        self.assertTrue(email2 in notification_email.recipients)
        self.assertTrue(email3 in notification_email.recipients)

    def test_send_email_with_context_dict(self):
        context = {"user": "2563468934986734986"}
        template = "emails/default.html"
        notification_email = NotificationEmail.objects.send_email(
            template=template, context=context
        )

        self.assertEqual(notification_email.context, context)
