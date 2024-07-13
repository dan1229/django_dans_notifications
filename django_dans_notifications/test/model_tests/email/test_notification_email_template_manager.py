from django.template import TemplateDoesNotExist
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
        # Create some templates to test with
        NotificationEmailTemplate.objects.create(
            path="django-dans-emails/default.html", nickname="default"
        )
        NotificationEmailTemplate.objects.create(
            path="emails/default.html", nickname="email_default"
        )

    # =================================================================== #
    # BASIC TESTS ======================================================= #
    # =================================================================== #

    def test_template_exists_by_path(self):
        template = "django-dans-emails/default.html"
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        self.assertEqual(email_template.path, template)

    def test_template_exists_by_path_without_emails(self):
        template = "default.html"
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        self.assertEqual(email_template.path, f"django-dans-emails/{template}")

    def test_template_exists_by_nickname(self):
        template = "default"
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        self.assertEqual(email_template.nickname, template)

    def test_template_does_not_exist_by_nickname(self):
        template = "nickname1"
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        self.assertIsNone(email_template)

    def test_template_does_not_exist_by_path(self):
        template = "django-dans-emails/invalid"
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        self.assertIsNone(email_template)

    def test_template_exists_in_emails_path(self):
        template = "default.html"
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        self.assertEqual(email_template.path, f"emails/{template}")

    def test_template_does_not_exist_and_is_created(self):
        template = "new_template.html"
        self.assertIsNone(
            NotificationEmailTemplate.objects.find_email_template(template)
        )
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        self.assertEqual(email_template.path, template)
        self.assertEqual(email_template.nickname, template)
