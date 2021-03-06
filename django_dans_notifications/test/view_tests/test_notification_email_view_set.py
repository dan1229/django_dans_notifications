import json
import uuid

from .base import BaseAPITestCase
from ...models.email import NotificationEmail
from ...views.email import NotificationEmailViewSet

"""
# =============================================================================================
# TEST NOTIFICATION EMAIL VIEW SET ============================================================
# =============================================================================================
"""


class TestNotificationEmailViewSet(BaseAPITestCase):
    def setUp(self):
        super(TestNotificationEmailViewSet, self).setUp()
        self.view_list = NotificationEmailViewSet.as_view({"get": "list"})
        self.view_retrieve = NotificationEmailViewSet.as_view({"get": "retrieve"})

    @staticmethod
    def get_url():
        return "/api/notifications/email/"

    @staticmethod
    def get_url_pk(pk):
        return f"/api/notifications/email/{pk}/"

    # ==================================================================================
    # GET - LIST =======================================================================
    # ==================================================================================

    def test_notifications_email_list_none(self):
        # make api request
        request = self.factory.get(
            self.get_url(), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_list(request)
        response.render()
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 0)
        self.assertEqual(json_response["next"], None)
        self.assertEqual(json_response["previous"], None)
        self.assertEqual(json_response["results"], [])

    def test_notification_email_list_one_not_recp(self):
        # create notification(s)
        notification1 = NotificationEmail.objects.create()

        # make api request
        request = self.factory.get(
            self.get_url(), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_list(request)
        response.render()
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 0)
        self.assertEqual(json_response["next"], None)
        self.assertEqual(json_response["previous"], None)

    def test_notification_email_list_one(self):
        # create notification(s)
        notification1 = NotificationEmail.objects.create(recipients=self.email)

        # make api request
        request = self.factory.get(
            self.get_url(), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_list(request)
        response.render()
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["next"], None)
        self.assertEqual(json_response["previous"], None)

    def test_notification_email_list_man_not_recp(self):
        # create notification(s)
        notification1 = NotificationEmail.objects.create()
        notification2 = NotificationEmail.objects.create()
        notification3 = NotificationEmail.objects.create()

        # make api request
        request = self.factory.get(
            self.get_url(), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_list(request)
        response.render()
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 0)
        self.assertEqual(json_response["next"], None)
        self.assertEqual(json_response["previous"], None)

    def test_notification_email_list_man_one_recp(self):
        # create notification(s)
        notification1 = NotificationEmail.objects.create(recipients=self.email)
        notification2 = NotificationEmail.objects.create()
        notification3 = NotificationEmail.objects.create()

        # make api request
        request = self.factory.get(
            self.get_url(), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_list(request)
        response.render()
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["next"], None)
        self.assertEqual(json_response["previous"], None)

    def test_notification_email_list_man_three_recp(self):
        # create notification(s)
        notification1 = NotificationEmail.objects.create(recipients=self.email)
        notification2 = NotificationEmail.objects.create(recipients=self.email)
        notification3 = NotificationEmail.objects.create(recipients=self.email)

        # make api request
        request = self.factory.get(
            self.get_url(), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_list(request)
        response.render()
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 3)
        self.assertEqual(json_response["next"], None)
        self.assertEqual(json_response["previous"], None)

    # ==================================================================================
    # GET - RETRIEVE ===================================================================
    # ==================================================================================

    def test_notification_email_retrieve_pk_valid_not_recp(self):
        # create notification(s)
        notification1 = NotificationEmail.objects.create()
        pk = notification1.pk

        # make api request
        request = self.factory.get(
            self.get_url_pk(pk=pk), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_retrieve(request, pk=pk)
        response.render()
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["error"], "Notification not found.")

    def test_notification_email_retrieve_pk_valid(self):
        # create notification(s)
        notification1 = NotificationEmail.objects.create(recipients=self.email)
        pk = notification1.pk

        # make api request
        request = self.factory.get(
            self.get_url_pk(pk=pk), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_retrieve(request, pk=pk)
        response.render()
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["success"]["id"], str(pk))

    def test_notification_email_retrieve_pk_valid_multiple_notification_email_not_recp(
        self,
    ):
        # create notification(s)
        notification1 = NotificationEmail.objects.create()
        notification2 = NotificationEmail.objects.create()
        notification3 = NotificationEmail.objects.create()
        pk = notification1.pk

        # make api request
        request = self.factory.get(
            self.get_url_pk(pk=pk), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_retrieve(request, pk=pk)
        response.render()
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["error"], "Notification not found.")

    def test_notification_email_retrieve_pk_valid_multiple_notification_email(self):
        # create notification(s)
        notification1 = NotificationEmail.objects.create(recipients=self.email)
        notification2 = NotificationEmail.objects.create()
        notification3 = NotificationEmail.objects.create()
        pk = notification1.pk

        # make api request
        request = self.factory.get(
            self.get_url_pk(pk=pk), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_retrieve(request, pk=pk)
        response.render()
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["success"]["id"], str(pk))

    def test_notification_email_retrieve_pk_invalid_uuid(self):
        # create notification(s)
        notification1 = NotificationEmail.objects.create()
        notification2 = NotificationEmail.objects.create()
        notification3 = NotificationEmail.objects.create()
        pk = "invalid"

        # make api request
        request = self.factory.get(
            self.get_url_pk(pk=pk), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_retrieve(request, pk=pk)
        response.render()
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["error"], "Notification not found.")

    def test_notification_email_retrieve_pk_missing(self):
        # create notification(s)
        notification1 = NotificationEmail.objects.create()
        notification2 = NotificationEmail.objects.create()
        notification3 = NotificationEmail.objects.create()
        pk = uuid.uuid4()

        # make api request
        request = self.factory.get(
            self.get_url_pk(pk=pk), HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_retrieve(request, pk=pk)
        response.render()
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["error"], "Notification not found.")
