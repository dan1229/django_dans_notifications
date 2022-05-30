from ..base import (
    BaseModelTestCase,
)
from ....models.basic import NotificationBasic

"""
# ========================================================================= #
# TEST BASIC NOTIFICATION ================================================= #
# ========================================================================= #
"""


class TestBasicNotification(BaseModelTestCase):
    model = NotificationBasic

    def setUp(self):
        super(TestBasicNotification, self).setUp()

    # =================================================================== #
    # BASIC TESTS ======================================================= #
    # =================================================================== #

    def test_str(self):
        self.notification = self.model.objects.create(
            recipients=self.base_email, sender=self.base_email
        )

        self.assertNotEqual(str(self.notification), None)

    def test_with_message(self):
        message = "this is a test message"
        self.notification = self.model.objects.create(
            recipients=self.base_email, sender=self.base_email, message=message
        )

        self.assertEqual(self.notification.message, message)

    # =================================================================== #
    # BASE NOTIFICATION TESTS =========================================== #
    # =================================================================== #
    #
    # NotificationBase is abstract, so we are unable to test it directly
    # it has methods and things used in all the notification models.
    # Said methods are tested here to ensure they're covered and not
    # 'doubled up on' in all the tests
    #
    #
    # RECIPIENT
    #
    def test_recipients_empty_str(self):
        recipients = ""
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(self.notification.recipients, "")
        self.assertEqual(self.notification.recipients, "")

    def test_recipients_empty_list(self):
        recipients = []
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(self.notification.recipients, "")
        self.assertEqual(self.notification.recipients, "")

    def test_recipients_list_of_one(self):
        email1 = "danielnazarian@outlook.com"
        recipients = [email1]
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertTrue(email1 in self.notification.recipients)

    def test_recipients_list_str_of_one(self):
        email1 = "danielnazarian@outlook.com"
        recipients = str([email1])
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertTrue(email1 in self.notification.recipients)

    def test_recipients_list_of_three(self):
        email1 = "danielnazarian@outlook.com"
        email2 = "danielnazarian+20@outlook.com"
        email3 = "danielnazarian+30@outlook.com"
        recipients = [email1, email2, email3]
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertTrue(email1 in self.notification.recipients)
        self.assertTrue(email2 in self.notification.recipients)
        self.assertTrue(email3 in self.notification.recipients)

    def test_recipients_list_str_of_three(self):
        email1 = "danielnazarian@outlook.com"
        email2 = "danielnazarian+20@outlook.com"
        email3 = "danielnazarian+30@outlook.com"
        recipients = str([email1, email2, email3])
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertTrue(email1 in self.notification.recipients)
        self.assertTrue(email2 in self.notification.recipients)
        self.assertTrue(email3 in self.notification.recipients)

    #
    # RECIPIENTS CONTAINS
    #
    def test_recipients_contains_empty_str(self):
        email1 = "danielnazarian@outlook.com"
        recipients = ""
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(self.notification.recipients, "")
        self.assertEqual(self.notification.recipients_contains(email1), False)

    def test_recipients_contains_empty_list(self):
        email1 = "danielnazarian@outlook.com"
        recipients = []
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(self.notification.recipients, "")
        self.assertEqual(self.notification.recipients_contains(email1), False)

    def test_recipients_contains_different_email(self):
        email1 = "danielnazarian@outlook.com"
        recipients = ["different@email.com"]
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(self.notification.recipients, recipients[0])
        self.assertEqual(self.notification.recipients_contains(email1), False)

    def test_recipients_contains_email(self):
        email1 = "danielnazarian@outlook.com"
        recipients = [email1]
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(self.notification.recipients, email1)
        self.assertEqual(self.notification.recipients_contains(email1), True)

    def test_recipients_contains_email_when_many(self):
        email1 = "danielnazarian@outlook.com"
        recipients = [
            "danielnazarian+20@outlook.com",
            email1,
            "danielnazarian+342345@outlook.com",
        ]
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(self.notification.recipients_contains(email1), True)

    def test_recipients_does_not_contain_email_when_many(self):
        email1 = "danielnazarian@outlook.com"
        recipients = [
            "danielnazarian+20@outlook.com",
            "danielnazarian+3253@outlook.com",
            "danielnazarian+342345@outlook.com",
        ]
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(self.notification.recipients_contains(email1), False)

    #
    # RECIPIENTS CLEANUP
    #
    def test_recipients_cleanup_empty_str(self):
        recipients = ""
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(self.notification.recipients_cleanup(), "")

    def test_recipients_cleanup_one_email_str(self):
        email1 = "danielnazarian@outlook.com"
        recipients = email1
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(self.notification.recipients_cleanup(), email1)

    def test_recipients_cleanup_one_email_list(self):
        email1 = "danielnazarian@outlook.com"
        recipients = [email1]
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(self.notification.recipients_cleanup(), email1)

    def test_recipients_cleanup_one_email_list_str(self):
        email1 = "danielnazarian@outlook.com"
        recipients = str([email1])
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(self.notification.recipients_cleanup(), email1)

    def test_recipients_cleanup_many_email_str(self):
        email1 = "danielnazarian@outlook.com"
        email2 = "danielnazarian+3523@outlook.com"
        email3 = "danielnazarian+436546@outlook.com"
        recipients = f"{email1},{email2},{email3}"
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        res = self.notification.recipients_cleanup()
        self.assertTrue(email1 in res)
        self.assertTrue(email2 in res)
        self.assertTrue(email3 in res)
        self.assertEqual(len(res.split(",")), 3)

    def test_recipients_cleanup_many_email_list(self):
        email1 = "danielnazarian@outlook.com"
        email2 = "danielnazarian+3523@outlook.com"
        email3 = "danielnazarian+436546@outlook.com"
        recipients = [email1, email2, email3]
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        res = self.notification.recipients_cleanup()
        self.assertTrue(email1 in res)
        self.assertTrue(email2 in res)
        self.assertTrue(email3 in res)
        self.assertEqual(len(res.split(",")), 3)

    def test_recipients_cleanup_many_email_list_str(self):
        email1 = "danielnazarian@outlook.com"
        email2 = "danielnazarian+3523@outlook.com"
        email3 = "danielnazarian+436546@outlook.com"
        recipients = str([email1, email2, email3])
        self.notification = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        res = self.notification.recipients_cleanup()
        self.assertTrue(email1 in res)
        self.assertTrue(email2 in res)
        self.assertTrue(email3 in res)
        self.assertEqual(len(res.split(",")), 3)
