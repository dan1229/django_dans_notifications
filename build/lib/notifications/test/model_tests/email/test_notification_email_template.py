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
        self.email_template_nickname = "template1"
        self.email_template = self.model.objects.create(
            nickname=self.email_template_nickname,
        )

        self.assertNotEqual(str(self.email_template), None)

    def test_with_path_exists(self):
        self.email_template_nickname = "template1"
        self.email_template_path = "emails/template.html"
        self.email_template = self.model.objects.create(
            nickname=self.email_template_nickname, path=self.email_template_path
        )

        self.assertEqual(self.email_template.path, self.email_template_path)

    def test_with_path_exists_no_extension(self):
        self.email_template_nickname = "template1"
        self.email_template_path = "emails/template"
        self.email_template = self.model.objects.create(
            nickname=self.email_template_nickname, path=self.email_template_path
        )

        self.assertEqual(self.email_template.path, self.email_template_path)

    def test_with_path_does_not_exist(self):
        self.email_template_nickname = "template1"
        self.email_template_path = "INVALID"
        self.email_template = self.model.objects.create(
            nickname=self.email_template_nickname, path=self.email_template_path
        )

        self.assertEqual(self.email_template.path, self.email_template_path)
