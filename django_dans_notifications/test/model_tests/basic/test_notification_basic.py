from typing import List
from ..base import BaseModelTestCase
from ....models.notifications import NotificationBasic

"""
# ========================================================================= #
# TEST BASIC NOTIFICATION ================================================= #
# ========================================================================= #
"""


class TestBasicNotification(BaseModelTestCase):
    model = NotificationBasic

    def setUp(self) -> None:
        super(TestBasicNotification, self).setUp()

    # =================================================================== #
    # BASIC TESTS ======================================================= #
    # =================================================================== #

    def test_str(self) -> None:
        notification: NotificationBasic = self.model.objects.create(
            recipients=self.base_email, sender=self.base_email
        )
        self.assertIsNotNone(str(notification))

    def test_with_message(self) -> None:
        message: str = "this is a test message"
        notification: NotificationBasic = self.model.objects.create(
            recipients=self.base_email, sender=self.base_email, message=message
        )
        self.assertEqual(notification.message, message)

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
    def test_recipients_empty_str(self) -> None:
        recipients: str = ""
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(notification.recipients, "")

    def test_recipients_empty_list(self) -> None:
        recipients: List[str] = []
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(notification.recipients, "")

    def test_recipients_list_of_one(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        recipients: List[str] = [email1]
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertIn(email1, notification.recipients)

    def test_recipients_list_str_of_one(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        recipients: str = str([email1])
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertIn(email1, notification.recipients)

    def test_recipients_list_of_three(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        email2: str = "danielnazarian+20@outlook.com"
        email3: str = "danielnazarian+30@outlook.com"
        recipients: List[str] = [email1, email2, email3]
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertIn(email1, notification.recipients)
        self.assertIn(email2, notification.recipients)
        self.assertIn(email3, notification.recipients)

    def test_recipients_list_str_of_three(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        email2: str = "danielnazarian+20@outlook.com"
        email3: str = "danielnazarian+30@outlook.com"
        recipients: str = str([email1, email2, email3])
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertIn(email1, notification.recipients)
        self.assertIn(email2, notification.recipients)
        self.assertIn(email3, notification.recipients)

    #
    # RECIPIENTS CONTAINS
    #
    def test_recipients_contains_empty_str(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        recipients: str = ""
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(notification.recipients, "")
        self.assertFalse(notification.recipients_contains(email1))

    def test_recipients_contains_empty_list(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        recipients: List[str] = []
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(notification.recipients, "")
        self.assertFalse(notification.recipients_contains(email1))

    def test_recipients_contains_different_email(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        recipients: List[str] = ["different@email.com"]
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(notification.recipients, recipients[0])
        self.assertFalse(notification.recipients_contains(email1))

    def test_recipients_contains_email(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        recipients: List[str] = [email1]
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(notification.recipients, email1)
        self.assertTrue(notification.recipients_contains(email1))

    def test_recipients_contains_email_when_many(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        recipients: List[str] = [
            "danielnazarian+20@outlook.com",
            email1,
            "danielnazarian+342345@outlook.com",
        ]
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertTrue(notification.recipients_contains(email1))

    def test_recipients_does_not_contain_email_when_many(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        recipients: List[str] = [
            "danielnazarian+20@outlook.com",
            "danielnazarian+3253@outlook.com",
            "danielnazarian+342345@outlook.com",
        ]
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertFalse(notification.recipients_contains(email1))

    #
    # RECIPIENTS CLEANUP
    #
    def test_recipients_cleanup_empty_str(self) -> None:
        recipients: str = ""
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(notification.recipients_cleanup(), "")

    def test_recipients_cleanup_one_email_str(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        recipients: str = email1
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(notification.recipients_cleanup(), email1)

    def test_recipients_cleanup_one_email_list(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        recipients: List[str] = [email1]
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(notification.recipients_cleanup(), email1)

    def test_recipients_cleanup_one_email_list_str(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        recipients: str = str([email1])
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        self.assertEqual(notification.recipients_cleanup(), email1)

    def test_recipients_cleanup_many_email_str(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        email2: str = "danielnazarian+3523@outlook.com"
        email3: str = "danielnazarian+436546@outlook.com"
        recipients: str = f"{email1},{email2},{email3}"
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        res: str = notification.recipients_cleanup()
        self.assertIn(email1, res)
        self.assertIn(email2, res)
        self.assertIn(email3, res)
        self.assertEqual(len(res.split(",")), 3)

    def test_recipients_cleanup_many_email_list(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        email2: str = "danielnazarian+3523@outlook.com"
        email3: str = "danielnazarian+436546@outlook.com"
        recipients: List[str] = [email1, email2, email3]
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        res: str = notification.recipients_cleanup()
        self.assertIn(email1, res)
        self.assertIn(email2, res)
        self.assertIn(email3, res)
        self.assertEqual(len(res.split(",")), 3)

    def test_recipients_cleanup_many_email_list_str(self) -> None:
        email1: str = "danielnazarian@outlook.com"
        email2: str = "danielnazarian+3523@outlook.com"
        email3: str = "danielnazarian+436546@outlook.com"
        recipients: str = str([email1, email2, email3])
        notification: NotificationBasic = self.model.objects.create(
            recipients=recipients, sender=self.base_email
        )
        res: str = notification.recipients_cleanup()
        self.assertIn(email1, res)
        self.assertIn(email2, res)
        self.assertIn(email3, res)
        self.assertEqual(len(res.split(",")), 3)
