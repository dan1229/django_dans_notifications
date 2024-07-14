import json
from typing import Any, Dict
import uuid
from .base import BaseAPITestCase
from ...models.notifications import NotificationPush
from ...views.push import NotificationPushViewSet

"""
# =============================================================================================
# TEST NOTIFICATION PUSH VIEW SET =============================================================
# =============================================================================================
"""


class TestNotificationPushViewSet(BaseAPITestCase):
    def setUp(self) -> None:
        super(TestNotificationPushViewSet, self).setUp()
        self.view_list = NotificationPushViewSet.as_view({"get": "list"})
        self.view_retrieve = NotificationPushViewSet.as_view({"get": "retrieve"})
        self.view_create = NotificationPushViewSet.as_view({"post": "create"})

    @staticmethod
    def get_url() -> str:
        return "/api/notifications/push/"

    @staticmethod
    def get_url_pk(pk: Any) -> str:
        return f"/api/notifications/push/{str(pk)}/"

    # ==================================================================================
    # GET - LIST =======================================================================
    # ==================================================================================

    def test_notifications_push_list_none(self) -> None:
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

    def test_notification_push_list_one_not_recp(self) -> None:
        # create notification(s)
        notification1 = NotificationPush.objects.create(message="Test message")

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

    def test_notification_push_list_one(self) -> None:
        # create notification(s)
        notification1 = NotificationPush.objects.create(
            recipients=self.email, message="Test message"
        )

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

    def test_notification_push_list_many_not_recp(self) -> None:
        # create notification(s)
        notification1 = NotificationPush.objects.create(message="Test message")
        notification2 = NotificationPush.objects.create(message="Test message 2")
        notification3 = NotificationPush.objects.create(message="Test message 3")

        # make api request
        request = self.factory.get(
            self.get_url(), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_list(request)
        response.render()  # type: ignore[attr-defined]  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 0)
        self.assertEqual(json_response["next"], None)
        self.assertEqual(json_response["previous"], None)
        self.assertEqual(json_response["results"], [])

    def test_notification_push_list_many_one_recp(self) -> None:
        # create notification(s)
        notification1 = NotificationPush.objects.create(
            recipients=self.email, message="Test message"
        )
        notification2 = NotificationPush.objects.create(message="Test message 2")
        notification3 = NotificationPush.objects.create(message="Test message 3")

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

    def test_notification_push_list_many_recp(self) -> None:
        # create notification(s)
        notification1 = NotificationPush.objects.create(
            recipients=self.email, message="Test message"
        )
        notification2 = NotificationPush.objects.create(
            recipients=self.email, message="Test message 2"
        )
        notification3 = NotificationPush.objects.create(
            recipients=self.email, message="Test message 3"
        )

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

    def test_notification_push_retrieve_pk_valid_not_recp(self) -> None:
        # create notification(s)
        notification1 = NotificationPush.objects.create(message="Test message")
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

    def test_notification_push_retrieve_pk_valid(self) -> None:
        # create notification(s)
        notification1 = NotificationPush.objects.create(
            recipients=self.email, message="Test message"
        )
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

    def test_notification_push_retrieve_pk_valid_multiple_notification_push_not_recp(
        self,
    ) -> None:
        # create notification(s)
        notification1 = NotificationPush.objects.create(message="Test message")
        notification2 = NotificationPush.objects.create(message="Test message 2")
        notification3 = NotificationPush.objects.create(message="Test message 3")
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

    def test_notification_push_retrieve_pk_valid_multiple_notification_push(
        self,
    ) -> None:
        # create notification(s)
        notification1 = NotificationPush.objects.create(
            recipients=self.email, message="Test message"
        )
        notification2 = NotificationPush.objects.create(message="Test message 2")
        notification3 = NotificationPush.objects.create(message="Test message 3")
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

    def test_notification_push_retrieve_pk_invalid_uuid(self) -> None:
        # create notification(s)
        notification1 = NotificationPush.objects.create(message="Test message")
        notification2 = NotificationPush.objects.create(message="Test message 2")
        notification3 = NotificationPush.objects.create(message="Test message 3")
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

    def test_notification_push_retrieve_pk_missing(self) -> None:
        # create notification(s)
        notification1 = NotificationPush.objects.create(message="Test message")
        notification2 = NotificationPush.objects.create(message="Test message 2")
        notification3 = NotificationPush.objects.create(message="Test message 3")
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

    def test_notification_push_create(self) -> None:
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

    def test_notification_push_create_missing_fields(self) -> None:
        data: Dict[Any, Any] = {}
        request = self.factory.post(
            self.get_url(), data, HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_create(request)
        response.render()  # type: ignore[attr-defined]
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Recipients required.")

    def test_notification_push_create_missing_message(self) -> None:
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
