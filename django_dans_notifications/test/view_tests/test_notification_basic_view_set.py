import json
from typing import Any, Dict
import uuid
from .base import BaseAPITestCase
from ...models.notifications import NotificationBasic
from ...views.basic import NotificationBasicViewSet

"""
# =============================================================================================
# TEST NOTIFICATION BASIC VIEW SET ============================================================
# =============================================================================================
"""


class TestNotificationBasicViewSet(BaseAPITestCase):
    def setUp(self) -> None:
        super(TestNotificationBasicViewSet, self).setUp()
        self.view_list = NotificationBasicViewSet.as_view({"get": "list"})
        self.view_retrieve = NotificationBasicViewSet.as_view({"get": "retrieve"})
        self.view_create = NotificationBasicViewSet.as_view({"post": "create"})
        self.view_update = NotificationBasicViewSet.as_view({"patch": "partial_update"})

    @staticmethod
    def get_url() -> str:
        return "/api/notifications/basic/"

    @staticmethod
    def get_url_pk(pk: Any) -> str:
        return f"/api/notifications/basic/{str(pk)}/"

    # ==================================================================================
    # GET - LIST =======================================================================
    # ==================================================================================

    def test_notifications_basic_list_none(self) -> None:
        # make api request
        request = self.factory.get(
            self.get_url(), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_list(request)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 0)
        self.assertEqual(json_response["next"], None)
        self.assertEqual(json_response["previous"], None)
        self.assertEqual(json_response["results"], [])

    def test_notification_basic_list_one_not_recp(self) -> None:
        # create notification(s)
        notification1 = NotificationBasic.objects.create()

        # make api request
        request = self.factory.get(
            self.get_url(), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_list(request)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 0)
        self.assertEqual(json_response["next"], None)
        self.assertEqual(json_response["previous"], None)

    def test_notification_basic_list_one(self) -> None:
        # create notification(s)
        notification1 = NotificationBasic.objects.create(recipients=self.email)

        # make api request
        request = self.factory.get(
            self.get_url(), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_list(request)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["next"], None)
        self.assertEqual(json_response["previous"], None)

    def test_notification_basic_list_man_not_recp(self) -> None:
        # create notification(s)
        notification1 = NotificationBasic.objects.create()
        notification2 = NotificationBasic.objects.create()
        notification3 = NotificationBasic.objects.create()

        # make api request
        request = self.factory.get(
            self.get_url(), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_list(request)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 0)
        self.assertEqual(json_response["next"], None)
        self.assertEqual(json_response["previous"], None)

    def test_notification_basic_list_man_one_recp(self) -> None:
        # create notification(s)
        notification1 = NotificationBasic.objects.create(recipients=self.email)
        notification2 = NotificationBasic.objects.create()
        notification3 = NotificationBasic.objects.create()

        # make api request
        request = self.factory.get(
            self.get_url(), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_list(request)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["next"], None)
        self.assertEqual(json_response["previous"], None)

    def test_notification_basic_list_man_three_recp(self) -> None:
        # create notification(s)
        notification1 = NotificationBasic.objects.create(recipients=self.email)
        notification2 = NotificationBasic.objects.create(recipients=self.email)
        notification3 = NotificationBasic.objects.create(recipients=self.email)

        # make api request
        request = self.factory.get(
            self.get_url(), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_list(request)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 3)
        self.assertEqual(json_response["next"], None)
        self.assertEqual(json_response["previous"], None)

    # ==================================================================================
    # GET - RETRIEVE ===================================================================
    # ==================================================================================

    def test_notification_basic_retrieve_pk_valid_not_recp(self) -> None:
        # create notification(s)
        notification1 = NotificationBasic.objects.create()
        pk = notification1.pk

        # make api request
        request = self.factory.get(
            self.get_url_pk(pk=pk), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_retrieve(request, pk=pk)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Notification not found.")

    def test_notification_basic_retrieve_pk_valid(self) -> None:
        # create notification(s)
        notification1 = NotificationBasic.objects.create(recipients=self.email)
        pk = notification1.pk

        # make api request
        request = self.factory.get(
            self.get_url_pk(pk=pk), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_retrieve(request, pk=pk)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["results"]["id"], str(pk))

    def test_notification_basic_retrieve_pk_valid_multiple_notification_basic_not_recp(
        self,
    ) -> None:
        # create notification(s)
        notification1 = NotificationBasic.objects.create()
        notification2 = NotificationBasic.objects.create()
        notification3 = NotificationBasic.objects.create()
        pk = notification1.pk

        # make api request
        request = self.factory.get(
            self.get_url_pk(pk=pk), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_retrieve(request, pk=pk)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Notification not found.")

    def test_notification_basic_retrieve_pk_valid_multiple_notification_basic(
        self,
    ) -> None:
        # create notification(s)
        notification1 = NotificationBasic.objects.create(recipients=self.email)
        notification2 = NotificationBasic.objects.create()
        notification3 = NotificationBasic.objects.create()
        pk = notification1.pk

        # make api request
        request = self.factory.get(
            self.get_url_pk(pk=pk), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_retrieve(request, pk=pk)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["results"]["id"], str(pk))

    def test_notification_basic_retrieve_pk_invalid_uuid(self) -> None:
        # create notification(s)
        notification1 = NotificationBasic.objects.create()
        notification2 = NotificationBasic.objects.create()
        notification3 = NotificationBasic.objects.create()
        pk = "invalid"

        # make api request
        request = self.factory.get(
            self.get_url_pk(pk=pk), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_retrieve(request, pk=pk)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Notification not found.")

    def test_notification_basic_retrieve_pk_missing(self) -> None:
        # create notification(s)
        notification1 = NotificationBasic.objects.create()
        notification2 = NotificationBasic.objects.create()
        notification3 = NotificationBasic.objects.create()
        pk = uuid.uuid4()

        # make api request
        request = self.factory.get(
            self.get_url_pk(pk=pk), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_retrieve(request, pk=pk)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Notification not found.")

    # ==================================================================================
    # POST - CREATE ====================================================================
    # ==================================================================================

    def test_notification_basic_create(self) -> None:
        data = {
            "recipients": self.email,
            "message": "Test message",
        }
        request = self.factory.post(
            self.get_url(), data, HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_create(request)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_response["results"]["recipients"], self.email)
        self.assertEqual(json_response["results"]["message"], "Test message")
        self.assertEqual(json_response["message"], "Successfully completed request.")

    def test_notification_basic_create_missing_fields(self) -> None:
        data: Dict[Any, Any] = {}
        request = self.factory.post(
            self.get_url(), data, HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_create(request)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Recipients required.")

    def test_notification_basic_create_missing_message(self) -> None:
        data = {
            "recipients": self.email,
        }
        request = self.factory.post(
            self.get_url(), data, HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_create(request)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Message required.")

    def test_notification_basic_create_invalid_recipients_validation_error(
        self,
    ) -> None:
        """Test that validation errors appear in error_fields key, not at top level"""
        data = {
            "recipients": ["not_a_string"],  # This should trigger a validation error
            "message": "Test message",
        }
        request = self.factory.post(
            self.get_url(),
            json.dumps(data),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.user_token}",
        )
        response = self.view_create(request)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        # Verify the response has the correct structure
        self.assertEqual(response.status_code, 400)
        self.assertIn("error_fields", json_response)
        self.assertIn("recipients", json_response["error_fields"])
        # Ensure recipients error is not at top level
        self.assertNotIn(
            "recipients", [k for k in json_response.keys() if k != "error_fields"]
        )
        self.assertEqual(
            json_response["message"],
            "Error creating notification. Please try again later.",
        )

    def test_notification_basic_create_multiple_validation_errors(self) -> None:
        """Test that validation error with extra long message appears in error_fields key"""
        # Create a message that exceeds the model's max_length of 600 chars
        long_message = "x" * 601
        data = {
            "recipients": ["not_a_string"],  # This should trigger a validation error
            "message": long_message,  # This should trigger max length validation error
        }
        request = self.factory.post(
            self.get_url(),
            json.dumps(data),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.user_token}",
        )
        response = self.view_create(request)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        # Verify the response has the correct structure
        self.assertEqual(response.status_code, 400)
        self.assertIn("error_fields", json_response)
        # Both fields should be in error_fields
        self.assertIn("recipients", json_response["error_fields"])
        self.assertIn("message", json_response["error_fields"])
        # Ensure recipients error is not at top level
        self.assertNotIn(
            "recipients", [k for k in json_response.keys() if k != "error_fields"]
        )

    # ==================================================================================
    # PATCH - PARTIAL UPDATE ===========================================================
    # ==================================================================================

    def test_notification_basic_partial_update(self) -> None:
        notification = NotificationBasic.objects.create(
            recipients=self.email, read=False
        )
        data = {"read": True}
        request = self.factory.patch(
            self.get_url_pk(notification.pk),
            data,
            HTTP_AUTHORIZATION=f"Token {self.user_token}",
        )
        response = self.view_update(request, pk=notification.pk)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["results"]["read"], True)

    def test_notification_basic_partial_update_invalid_uuid(self) -> None:
        data = {"read": True}
        request = self.factory.patch(
            self.get_url_pk("invalid"),
            data,
            HTTP_AUTHORIZATION=f"Token {self.user_token}",
        )
        response = self.view_update(request, pk="invalid")
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Notification not found.")
