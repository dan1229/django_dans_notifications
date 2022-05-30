from ..base import BaseModelTestCase
from ....models.email import NotificationEmailTemplate

"""
# ========================================================================= #
# TEST NOTIFICATION EMAIL TEMPLATE MANAGER ================================ #
# ========================================================================= #
"""


class TestNotificationEmailTemplateManager(BaseModelTestCase):
    email = "test+1@example.com"
    password = "password"

    def setUp(self):
        super(TestNotificationEmailTemplateManager, self).setUp()

    # =================================================================== #
    # BASIC TESTS ======================================================= #
    # =================================================================== #

    def test_template_exists_by_path(self):
        template = "emails/default.html"
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        self.assertEqual(email_template.path, template)

    def test_template_exists_by_path_without_emails(self):
        template = "default.html"
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        self.assertEqual(email_template.path, template)

    def test_template_exists_by_nickname(self):
        template = "nickname1"
        NotificationEmailTemplate.objects.create(nickname=template)
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        self.assertEqual(email_template.nickname, template)

    def test_template_does_not_exists_by_nickname(self):
        template = "nickname1"
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        self.assertEqual(email_template, None)

    def test_template_does_not_exists_by_path(self):
        template = "emails/invalid"
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        self.assertEqual(email_template, None)
