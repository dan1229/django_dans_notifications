from ..base import BaseModelTestCase
from ....models.email import NotificationEmailTemplate

"""
# ========================================================================= #
# TEST EMAIL NOTIFICATION TEMPLATE ======================================== #
# ========================================================================= #
"""


class TestEmailNotificationTemplate(BaseModelTestCase):
    model = NotificationEmailTemplate

    def setUp(self):
        super(TestEmailNotificationTemplate, self).setUp()

    # =================================================================== #
    # BASIC TESTS ======================================================= #
    # =================================================================== #

    def test_str(self):
        email_template = self.model.objects.create(
            nickname="template1",
        )
        self.assertEqual(str(email_template), "Email Template: template1")

    def test_with_path_exists(self):
        email_template = self.model.objects.create(
            nickname="template1", path="django-dans-emails/template.html"
        )
        self.assertEqual(email_template.path, "django-dans-emails/template.html")

    def test_with_path_exists_no_extension(self):
        email_template = self.model.objects.create(
            nickname="template1", path="django-dans-emails/template"
        )
        self.assertEqual(email_template.path, "django-dans-emails/template")

    def test_with_path_does_not_exist(self):
        email_template = self.model.objects.create(nickname="template1", path="INVALID")
        self.assertEqual(email_template.path, "INVALID")

    def test_html_to_str_template_exists(self):
        email_template = self.model.objects.create(
            nickname="template1", path="django-dans-emails/template.html"
        )
        rendered_string = email_template.html_to_str({})
        self.assertIn(
            "CONTENT", rendered_string
        )  # this is the content of the template template

    def test_html_to_str_template_exists_context_irrelevant(self):
        email_template = self.model.objects.create(
            nickname="template1", path="django-dans-emails/template.html"
        )
        rendered_string = email_template.html_to_str(
            {"key": "value"}
        )  # shouldn't change anything
        self.assertIn(
            "CONTENT", rendered_string
        )  # this is the content of the template template

    def test_html_to_str_template_does_not_exist(self):
        email_template = self.model.objects.create(nickname="template1", path="INVALID")
        with self.assertLogs("django_dans_notifications", level="ERROR") as log:
            rendered_string = email_template.html_to_str({"key": "value"})
            self.assertIn("Error rendering email template", log.output[0])
            # Ensure the default template is rendered in case of failure
            self.assertIn("This is an email.", rendered_string)
