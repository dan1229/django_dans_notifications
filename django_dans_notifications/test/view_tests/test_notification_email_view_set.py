import json
from typing import Any
import uuid
from .base import BaseAPITestCase
from ...models.notifications import NotificationEmail, NotificationEmailTemplate
from ...views.email import NotificationEmailViewSet

"""
# =============================================================================================
# TEST NOTIFICATION EMAIL VIEW SET ============================================================
# =============================================================================================
"""


class TestNotificationEmailViewSet(BaseAPITestCase):
    def setUp(self) -> None:
        super(TestNotificationEmailViewSet, self).setUp()
        self.view_list = NotificationEmailViewSet.as_view({"get": "list"})
        self.view_retrieve = NotificationEmailViewSet.as_view({"get": "retrieve"})

        self.email_template = NotificationEmailTemplate.objects.create(
            nickname="default", path="django-dans-emails/default.html"
        )

    @staticmethod
    def get_url() -> str:
        return "/api/notifications/email/"

    @staticmethod
    def get_url_pk(pk: Any) -> str:
        return f"/api/notifications/email/{str(pk)}/"

    # ==================================================================================
    # GET - LIST =======================================================================
    # ==================================================================================

    def test_notifications_email_list_none(self) -> None:
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

    def test_notification_email_list_one_not_recp(self) -> None:
        # create notification(s)
        notification1 = NotificationEmail.objects.create(
            subject="Test Subject",
            context={"key": "value"},
            template=self.email_template,
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
        self.assertEqual(json_response["count"], 0)
        self.assertEqual(json_response["next"], None)
        self.assertEqual(json_response["previous"], None)

    def test_notification_email_list_one(self) -> None:
        # create notification(s)
        notification1 = NotificationEmail.objects.create(
            recipients=self.email,
            subject="Test Subject",
            context={"key": "value"},
            template=self.email_template,
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

    def test_notification_email_list_many_not_recp(self) -> None:
        # create notification(s)
        notification1 = NotificationEmail.objects.create(
            subject="Test Subject",
            context={"key": "value"},
            template=self.email_template,
        )
        notification2 = NotificationEmail.objects.create(
            subject="Test Subject 2",
            context={"key": "value"},
            template=self.email_template,
        )
        notification3 = NotificationEmail.objects.create(
            subject="Test Subject 3",
            context={"key": "value"},
            template=self.email_template,
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
        self.assertEqual(json_response["count"], 0)
        self.assertEqual(json_response["next"], None)
        self.assertEqual(json_response["previous"], None)

    def test_notification_email_list_many_one_recp(self) -> None:
        # create notification(s)
        notification1 = NotificationEmail.objects.create(
            recipients=self.email,
            subject="Test Subject",
            context={"key": "value"},
            template=self.email_template,
        )
        notification2 = NotificationEmail.objects.create(
            subject="Test Subject 2",
            context={"key": "value"},
            template=self.email_template,
        )
        notification3 = NotificationEmail.objects.create(
            subject="Test Subject 3",
            context={"key": "value"},
            template=self.email_template,
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

    def test_notification_email_list_many_recp(self) -> None:
        # create notification(s)
        notification1 = NotificationEmail.objects.create(
            recipients=self.email,
            subject="Test Subject",
            context={"key": "value"},
            template=self.email_template,
        )
        notification2 = NotificationEmail.objects.create(
            recipients=self.email,
            subject="Test Subject 2",
            context={"key": "value"},
            template=self.email_template,
        )
        notification3 = NotificationEmail.objects.create(
            recipients=self.email,
            subject="Test Subject 3",
            context={"key": "value"},
            template=self.email_template,
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

    def test_notification_email_retrieve_pk_valid_not_recp(self) -> None:
        # create notification(s)
        notification1 = NotificationEmail.objects.create(
            subject="Test Subject",
            context={"key": "value"},
            template=self.email_template,
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
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Notification not found.")

    def test_notification_email_retrieve_pk_valid(self) -> None:
        # create notification(s)
        notification1 = NotificationEmail.objects.create(
            recipients=self.email,
            subject="Test Subject",
            context={"key": "value"},
            template=self.email_template,
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

    def test_notification_email_retrieve_pk_valid_multiple_notification_email_not_recp(
        self,
    ) -> None:
        # create notification(s)
        notification1 = NotificationEmail.objects.create(
            subject="Test Subject",
            context={"key": "value"},
            template=self.email_template,
        )
        notification2 = NotificationEmail.objects.create(
            subject="Test Subject 2",
            context={"key": "value"},
            template=self.email_template,
        )
        notification3 = NotificationEmail.objects.create(
            subject="Test Subject 3",
            context={"key": "value"},
            template=self.email_template,
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
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Notification not found.")

    def test_notification_email_retrieve_pk_valid_multiple_notification_email(
        self,
    ) -> None:
        # create notification(s)
        notification1 = NotificationEmail.objects.create(
            recipients=self.email,
            subject="Test Subject",
            context={"key": "value"},
            template=self.email_template,
        )
        notification2 = NotificationEmail.objects.create(
            subject="Test Subject 2",
            context={"key": "value"},
            template=self.email_template,
        )
        notification3 = NotificationEmail.objects.create(
            subject="Test Subject 3",
            context={"key": "value"},
            template=self.email_template,
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

    def test_notification_email_retrieve_pk_invalid_uuid(self) -> None:
        # create notification(s)
        notification1 = NotificationEmail.objects.create(
            subject="Test Subject",
            context={"key": "value"},
            template=self.email_template,
        )
        notification2 = NotificationEmail.objects.create(
            subject="Test Subject 2",
            context={"key": "value"},
            template=self.email_template,
        )
        notification3 = NotificationEmail.objects.create(
            subject="Test Subject 3",
            context={"key": "value"},
            template=self.email_template,
        )
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

    def test_notification_email_retrieve_pk_missing(self) -> None:
        # create notification(s)
        notification1 = NotificationEmail.objects.create(
            subject="Test Subject",
            context={"key": "value"},
            template=self.email_template,
        )
        notification2 = NotificationEmail.objects.create(
            subject="Test Subject 2",
            context={"key": "value"},
            template=self.email_template,
        )
        notification3 = NotificationEmail.objects.create(
            subject="Test Subject 3",
            context={"key": "value"},
            template=self.email_template,
        )
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
