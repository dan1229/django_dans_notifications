from ..base import BaseModelTestCase
from ....models.notifications import NotificationEmailTemplate

"""
# ========================================================================= #
# TEST NOTIFICATION EMAIL TEMPLATE MANAGER ================================ #
# ========================================================================= #
"""


class TestNotificationEmailTemplateManager(BaseModelTestCase):
    email = "test+1@example.com"
    password = "password"

    def setUp(self) -> None:
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

    def test_template_exists_by_path(self) -> None:
        template = "django-dans-emails/default.html"
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        if email_template is None:
            self.fail("Email template not found")
        self.assertEqual(email_template.path, template)

    def test_template_exists_by_path_without_emails(self) -> None:
        template = "default.html"
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        if email_template is None:
            self.fail("Email template not found")
        self.assertEqual(email_template.path, f"django-dans-emails/{template}")

    def test_template_exists_by_nickname(self) -> None:
        template = "default"
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        if email_template is None:
            self.fail("Email template not found")
        self.assertEqual(email_template.nickname, template)

    def test_template_does_not_exist_by_nickname(self) -> None:
        template = "nickname1"
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        if email_template is not None:
            self.fail("Email template found")
        self.assertIsNone(email_template)

    def test_template_does_not_exist_by_path(self) -> None:
        template = "django-dans-emails/invalid"
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        if email_template is not None:
            self.fail("Email template found")
        self.assertIsNone(email_template)

    def test_template_exists_in_emails_path(self) -> None:
        template = "default.html"
        email_template = NotificationEmailTemplate.objects.find_email_template(
            f"emails/{template}"
        )
        if email_template is None:
            self.fail("Email template not found")
        self.assertEqual(email_template.path, f"emails/{template}")

    def test_template_exists_in_django_dans_path(self) -> None:
        template = "default.html"
        email_template = NotificationEmailTemplate.objects.find_email_template(
            f"django-dans-emails/{template}"
        )
        if email_template is None:
            self.fail("Email template not found")
        self.assertEqual(email_template.path, f"django-dans-emails/{template}")

    def test_template_does_not_exist(self) -> None:
        template = "new_template.html"
        email_template = NotificationEmailTemplate.objects.find_email_template(template)
        if email_template is not None:
            self.fail("Email template found")
        self.assertIsNone(email_template)
