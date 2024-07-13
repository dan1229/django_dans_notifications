from django.core.files.uploadedfile import SimpleUploadedFile
from ..base import BaseModelTestCase
from ....models.email import NotificationEmail
from ....logging import LOGGER

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
        with self.assertRaises(ValueError):
            NotificationEmail.objects.send_email(
                template="INVALID",
            )

    def test_send_email_template_does_exist(self):
        template = "django-dans-emails/default.html"
        notification_email = NotificationEmail.objects.send_email(
            template=template,
        )
        self.assertEqual(notification_email.template.path, template)

    def test_send_email_no_recipients(self):
        template = "django-dans-emails/default.html"
        recipients = []
        notification_email = NotificationEmail.objects.send_email(
            template=template, recipients=recipients
        )
        self.assertEqual(notification_email.recipients, "")

    def test_send_email_with_one_recipient_list(self):
        email1 = "danielnazarian@outlook.com"
        template = "django-dans-emails/default.html"
        recipients = [email1]
        notification_email = NotificationEmail.objects.send_email(
            template=template, recipients=recipients
        )
        self.assertEqual(notification_email.recipients, email1)

    def test_send_email_with_one_recipient_str(self):
        email1 = "danielnazarian@outlook.com"
        template = "django-dans-emails/default.html"
        recipients = str([email1])
        notification_email = NotificationEmail.objects.send_email(
            template=template, recipients=recipients
        )
        self.assertEqual(notification_email.recipients, email1)

    def test_send_email_with_many_recipients_list(self):
        email1 = "danielnazarian@outlook.com"
        email2 = "danielnazarian+32523@outlook.com"
        email3 = "danielnazarian+352346@outlook.com"
        template = "django-dans-emails/default.html"
        recipients = [email1, email2, email3]
        notification_email = NotificationEmail.objects.send_email(
            template=template, recipients=recipients
        )
        self.assertIn(email1, notification_email.recipients)
        self.assertIn(email2, notification_email.recipients)
        self.assertIn(email3, notification_email.recipients)

    def test_send_email_with_many_recipients_str(self):
        email1 = "danielnazarian@outlook.com"
        email2 = "danielnazarian+32523@outlook.com"
        email3 = "danielnazarian+352346@outlook.com"
        template = "django-dans-emails/default.html"
        recipients = str([email1, email2, email3])
        notification_email = NotificationEmail.objects.send_email(
            template=template, recipients=recipients
        )
        self.assertIn(email1, notification_email.recipients)
        self.assertIn(email2, notification_email.recipients)
        self.assertIn(email3, notification_email.recipients)

    def test_send_email_with_context_dict(self):
        context = {"user": "2563468934986734986"}
        template = "django-dans-emails/default.html"
        notification_email = NotificationEmail.objects.send_email(
            template=template, context=context
        )
        self.assertEqual(notification_email.context, context)

    def test_send_email_with_file_attachment(self):
        template = "django-dans-emails/default.html"
        file_attachment = SimpleUploadedFile("file.txt", b"file_content")

        # Capture logs
        with self.assertLogs(LOGGER, level="DEBUG") as log:
            notification_email = NotificationEmail.objects.send_email(
                template=template, file_attachment=file_attachment
            )

        self.assertIsNotNone(notification_email)

        # Check that the attachment debug log is present
        self.assertTrue(
            any("File attachment successful." in message for message in log.output)
        )

    def test_send_email_with_subject_and_sender(self):
        subject = "Custom Subject"
        sender = "customsender@example.com"
        template = "django-dans-emails/default.html"
        notification_email = NotificationEmail.objects.send_email(
            subject=subject, template=template, sender=sender
        )
        self.assertEqual(notification_email.subject, subject)
        self.assertEqual(notification_email.sender, sender)

    def test_send_email_does_not_send_in_test_mode(self):
        with self.settings(IN_TEST=True):
            template = "django-dans-emails/default.html"
            notification_email = NotificationEmail.objects.send_email(template=template)
            # Ensure email is not marked as sent in test mode
            self.assertFalse(notification_email.sent_successfully)
