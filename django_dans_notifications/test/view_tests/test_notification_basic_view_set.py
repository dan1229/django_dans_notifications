import json
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
    def setUp(self):
        super(TestNotificationBasicViewSet, self).setUp()
        self.view_list = NotificationBasicViewSet.as_view({"get": "list"})
        self.view_retrieve = NotificationBasicViewSet.as_view({"get": "retrieve"})
        self.view_create = NotificationBasicViewSet.as_view({"post": "create"})
        self.view_update = NotificationBasicViewSet.as_view({"patch": "partial_update"})

    @staticmethod
    def get_url():
        return "/api/notifications/basic/"

    @staticmethod
    def get_url_pk(pk):
        return f"/api/notifications/basic/{pk}/"

    # ==================================================================================
    # GET - LIST =======================================================================
    # ==================================================================================

    def test_notifications_basic_list_none(self):
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

    def test_notification_basic_list_one_not_recp(self):
        # create notification(s)
        notification1 = NotificationBasic.objects.create()

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

    def test_notification_basic_list_one(self):
        # create notification(s)
        notification1 = NotificationBasic.objects.create(recipients=self.email)

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

    def test_notification_basic_list_man_not_recp(self):
        # create notification(s)
        notification1 = NotificationBasic.objects.create()
        notification2 = NotificationBasic.objects.create()
        notification3 = NotificationBasic.objects.create()

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

    def test_notification_basic_list_man_one_recp(self):
        # create notification(s)
        notification1 = NotificationBasic.objects.create(recipients=self.email)
        notification2 = NotificationBasic.objects.create()
        notification3 = NotificationBasic.objects.create()

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

    def test_notification_basic_list_man_three_recp(self):
        # create notification(s)
        notification1 = NotificationBasic.objects.create(recipients=self.email)
        notification2 = NotificationBasic.objects.create(recipients=self.email)
        notification3 = NotificationBasic.objects.create(recipients=self.email)

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

    def test_notification_basic_retrieve_pk_valid_not_recp(self):
        # create notification(s)
        notification1 = NotificationBasic.objects.create()
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
        self.assertEqual(json_response["message"], "Notification not found.")

    def test_notification_basic_retrieve_pk_valid(self):
        # create notification(s)
        notification1 = NotificationBasic.objects.create(recipients=self.email)
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
        self.assertEqual(json_response["results"]["id"], str(pk))

    def test_notification_basic_retrieve_pk_valid_multiple_notification_basic_not_recp(
        self,
    ):
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
        response.render()
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Notification not found.")

    def test_notification_basic_retrieve_pk_valid_multiple_notification_basic(self):
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
        response.render()
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["results"]["id"], str(pk))

    def test_notification_basic_retrieve_pk_invalid_uuid(self):
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
        response.render()
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Notification not found.")

    def test_notification_basic_retrieve_pk_missing(self):
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
        response.render()
        json_response = json.loads(response.content)

        # confirm status code and data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Notification not found.")

    # ==================================================================================
    # POST - CREATE ====================================================================
    # ==================================================================================

    def test_notification_basic_create(self):
        data = {
            "recipients": self.email,
            "message": "Test message",
        }
        request = self.factory.post(
            self.get_url(), data, HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_create(request)
        response.render()
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_response["results"]["recipients"], self.email)
        self.assertEqual(json_response["results"]["message"], "Test message")
        self.assertEqual(json_response["message"], "Successfully completed request.")

    def test_notification_basic_create_missing_fields(self):
        data = {}
        request = self.factory.post(
            self.get_url(), data, HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_create(request)
        response.render()
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Recipients required.")

    def test_notification_basic_create_missing_message(self):

        data = {
            "recipients": self.email,
        }
        request = self.factory.post(
            self.get_url(), data, HTTP_AUTHORIZATION=f"Token {self.user_token}"
        )
        response = self.view_create(request)
        response.render()
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Message required.")

    # ==================================================================================
    # PATCH - PARTIAL UPDATE ===========================================================
    # ==================================================================================

    def test_notification_basic_partial_update(self):
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
        response.render()
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["results"]["read"], True)

    def test_notification_basic_partial_update_invalid_uuid(self):
        data = {"read": True}
        request = self.factory.patch(
            self.get_url_pk("invalid"),
            data,
            HTTP_AUTHORIZATION=f"Token {self.user_token}",
        )
        response = self.view_update(request, pk="invalid")
        response.render()
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Notification not found.")
