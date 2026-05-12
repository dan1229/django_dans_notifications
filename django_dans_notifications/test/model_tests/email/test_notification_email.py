from smtplib import SMTPException
from unittest.mock import patch

from django.test.utils import override_settings

from ..base import BaseModelTestCase
from ....email_sender import EmailSender
from ....models.notifications import NotificationEmail, NotificationEmailTemplate

"""
# ========================================================================= #
# TEST EMAIL NOTIFICATION ================================================= #
# ========================================================================= #
"""


class TestEmailNotification(BaseModelTestCase):
    model = NotificationEmail

    def setUp(self) -> None:
        self.email_template_nickname = "template1"
        self.email_template = NotificationEmailTemplate.objects.create(
            nickname=self.email_template_nickname,
            path="django-dans-emails/template.html",
        )
        super(TestEmailNotification, self).setUp()

    def _reset_email_sender(self) -> None:
        # EmailSender caches async/sync mode on the singleton at first init,
        # so override_settings won't take effect unless we reset it.
        if EmailSender._instance and EmailSender._instance._executor:
            EmailSender._instance.shutdown(wait=False)
        EmailSender._instance = None
        EmailSender._executor = None

    # =================================================================== #
    # BASIC TESTS ======================================================= #
    # =================================================================== #

    def test_str(self) -> None:
        notification = self.model.objects.create(
            template=self.email_template,
            recipients=self.base_email,
            sender=self.base_email,
        )
        self.assertEqual(
            str(notification),
            f"Notification Email: {self.base_email} -> {self.base_email}",
        )

    def test_with_subject(self) -> None:
        subject = "this is a test subject"
        notification = self.model.objects.create(
            template=self.email_template,
            recipients=self.base_email,
            sender=self.base_email,
            subject=subject,
        )
        self.assertEqual(notification.subject, subject)

    def test_with_context(self) -> None:
        context = {"user": "213542465346"}
        notification = self.model.objects.create(
            template=self.email_template,
            recipients=self.base_email,
            sender=self.base_email,
            context=context,
        )
        self.assertEqual(notification.context, context)

    def test_with_no_template(self) -> None:
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

    def test_with_recipients(self) -> None:
        recipients = ["user1@example.com", "user2@example.com"]
        notification = self.model.objects.create(
            template=self.email_template, recipients=recipients, sender=self.base_email
        )
        self.assertEqual(notification.recipients, ",".join(recipients))

    # =================================================================== #
    # SEND_EMAIL OUTCOME TESTS ========================================== #
    # =================================================================== #

    @override_settings(IN_TEST=False, EMAIL_SYNC_MODE=True, EMAIL_RETRY_DELAY=0.0)
    def test_send_email_marks_successful_after_smtp_resolves(self) -> None:
        """sent_successfully is True only after SMTP returns without raising."""
        self._reset_email_sender()
        try:
            with patch(
                "django.core.mail.EmailMultiAlternatives.send", return_value=1
            ) as mock_send:
                notification = self.model.objects.send_email(
                    subject="Sync OK",
                    template=self.email_template_nickname,
                    sender=self.base_email,
                    recipients=self.base_email,
                )
            mock_send.assert_called()
            self.assertTrue(notification.sent_successfully)
            notification.refresh_from_db()
            self.assertTrue(notification.sent_successfully)
        finally:
            self._reset_email_sender()

    @override_settings(
        IN_TEST=False,
        EMAIL_SYNC_MODE=True,
        EMAIL_MAX_RETRIES=2,
        EMAIL_RETRY_DELAY=0.0,
    )
    def test_send_email_marks_failed_when_smtp_raises(self) -> None:
        """sent_successfully stays False when SMTP send raises after all retries."""
        self._reset_email_sender()
        try:
            with patch(
                "django.core.mail.EmailMultiAlternatives.send",
                side_effect=SMTPException("connection refused"),
            ):
                notification = self.model.objects.send_email(
                    subject="Sync Fail",
                    template=self.email_template_nickname,
                    sender=self.base_email,
                    recipients=self.base_email,
                )
            self.assertFalse(notification.sent_successfully)
            notification.refresh_from_db()
            self.assertFalse(notification.sent_successfully)
        finally:
            self._reset_email_sender()

    @override_settings(
        IN_TEST=False,
        EMAIL_SYNC_MODE=False,
        EMAIL_MAX_WORKERS=2,
        EMAIL_RETRY_DELAY=0.0,
    )
    def test_send_email_async_callback_updates_row(self) -> None:
        """Async path: callback writes sent_successfully=True after the future resolves."""
        self._reset_email_sender()
        try:
            with patch("django.core.mail.EmailMultiAlternatives.send", return_value=1):
                notification = self.model.objects.send_email(
                    subject="Async OK",
                    template=self.email_template_nickname,
                    sender=self.base_email,
                    recipients=self.base_email,
                )
            # Drain the executor so the done-callback completes before we
            # inspect the row.
            sender = EmailSender()
            if sender._executor is not None:
                sender._executor.shutdown(wait=True)
            notification.refresh_from_db()
            self.assertTrue(notification.sent_successfully)
        finally:
            self._reset_email_sender()
