from typing import List, Dict, Any
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from unittest.mock import patch
from ..base import BaseModelTestCase
from ....models.notifications import NotificationEmail
from ....logging import LOGGER

"""
# ========================================================================= #
# TEST NOTIFICATION EMAIL MANAGER ========================================= #
# ========================================================================= #
"""


class TestNotificationEmailManager(BaseModelTestCase):
    email: str = "test+1@example.com"
    password: str = "password"

    def setUp(self) -> None:
        super(TestNotificationEmailManager, self).setUp()  # type: ignore[no-untyped-call]

    # =================================================================== #
    # BASIC TESTS ======================================================= #
    # =================================================================== #

    def test_send_email_template_doesnt_exist(self) -> None:
        with self.assertRaises(ValueError):
            NotificationEmail.objects.send_email(
                "",
                template="INVALID",
            )

    def test_send_email_template_does_exist(self) -> None:
        template: str = "django-dans-emails/default.html"
        notification_email: NotificationEmail = NotificationEmail.objects.send_email(
            "",
            template=template,
        )
        self.assertEqual(notification_email.template.path, template)

    def test_send_email_no_recipients(self) -> None:
        template: str = "django-dans-emails/default.html"
        recipients: List[str] = []
        notification_email: NotificationEmail = NotificationEmail.objects.send_email(
            template=template, recipients=recipients
        )
        self.assertEqual(notification_email.recipients, "")

    def test_send_email_with_one_recipient_list(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        template: str = "django-dans-emails/default.html"
        recipients: List[str] = [email1]
        notification_email: NotificationEmail = NotificationEmail.objects.send_email(
            template=template, recipients=recipients
        )
        self.assertEqual(notification_email.recipients, email1)

    def test_send_email_with_one_recipient_str(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        template: str = "django-dans-emails/default.html"
        recipients: str = str([email1])
        notification_email: NotificationEmail = NotificationEmail.objects.send_email(
            template=template, recipients=recipients
        )
        self.assertEqual(notification_email.recipients, email1)

    def test_send_email_with_many_recipients_list(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        email2: str = "danielnazarian+32523@outlook.com"
        email3: str = "danielnazarian+352346@outlook.com"
        template: str = "django-dans-emails/default.html"
        recipients: List[str] = [email1, email2, email3]
        notification_email: NotificationEmail = NotificationEmail.objects.send_email(
            recipients=recipients, template=template
        )
        self.assertIn(email1, notification_email.recipients)
        self.assertIn(email2, notification_email.recipients)
        self.assertIn(email3, notification_email.recipients)

    def test_send_email_with_many_recipients_str(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        email2: str = "danielnazarian+32523@outlook.com"
        email3: str = "danielnazarian+352346@outlook.com"
        template: str = "django-dans-emails/default.html"
        recipients: str = str([email1, email2, email3])
        notification_email: NotificationEmail = NotificationEmail.objects.send_email(
            template=template, recipients=recipients
        )
        self.assertIn(email1, notification_email.recipients)
        self.assertIn(email2, notification_email.recipients)
        self.assertIn(email3, notification_email.recipients)

    def test_send_email_with_context_dict(self) -> None:
        context: Dict[str, Any] = {"user": "2563468934986734986"}
        template: str = "django-dans-emails/default.html"
        notification_email: NotificationEmail = NotificationEmail.objects.send_email(
            template=template, context=context
        )
        self.assertEqual(notification_email.context, context)

    def test_send_email_with_file_attachment(self) -> None:
        template: str = "django-dans-emails/default.html"
        file_attachment: SimpleUploadedFile = SimpleUploadedFile(
            "file.txt", b"file_content"
        )

        # Capture logs
        with self.assertLogs(LOGGER, level="DEBUG") as log:
            notification_email: NotificationEmail = (
                NotificationEmail.objects.send_email(
                    template=template, file_attachment=file_attachment
                )
            )
            # Check that the attachment error log is present
            self.assertTrue(
                any("File attached to email" in message for message in log.output)
            )
            # Check that the attachment error log is NOT present
            self.assertFalse(
                any("Issue attaching to email" in message for message in log.output)
            )

        self.assertIsNotNone(notification_email)

    def test_send_email_with_invalid_file_attachment(self) -> None:
        template: str = "django-dans-emails/default.html"

        # Create an invalid file object
        invalid_file: SimpleUploadedFile = SimpleUploadedFile("invalid_file.txt", b"")

        # Mock the read method to raise an AttributeError
        with patch.object(File, "read", side_effect=AttributeError("Invalid file")):
            with self.assertLogs(LOGGER, level="ERROR") as log:
                notification_email = (
                    NotificationEmail.objects.send_email(
                        template=template, file_attachment=invalid_file
                    ),
                )[0]
                # Check that the attachment error log is present
                self.assertTrue(
                    any("Issue attaching to email" in message for message in log.output)
                )

            self.assertIsNotNone(notification_email)

    def test_send_email_with_subject_and_sender(self) -> None:
        subject: str = "Custom Subject"
        sender: str = "customsender@example.com"
        template: str = "django-dans-emails/default.html"
        notification_email: NotificationEmail = NotificationEmail.objects.send_email(
            subject=subject, template=template, sender=sender
        )
        self.assertEqual(notification_email.subject, subject)
        self.assertEqual(notification_email.sender, sender)

    def test_send_email_does_not_send_in_test_mode(self) -> None:
        with self.settings(IN_TEST=True):
            template: str = "django-dans-emails/default.html"
            notification_email: NotificationEmail = (
                NotificationEmail.objects.send_email(template=template)
            )
            # Ensure email is not marked as sent in test mode
            self.assertFalse(notification_email.sent_successfully)
