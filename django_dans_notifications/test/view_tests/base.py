from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory


"""
# =============================================================================================
# BASE API TEST CASE ==========================================================================
# =============================================================================================
"""


class BaseAPITestCase(APITestCase):
    username = "testuser1"
    email = "test@test.com"
    username = "api-test-user"
    password = "password"

    def setUp(self):
        super(APITestCase, self).setUp()

        # store standard api factory
        self.factory = APIRequestFactory()

        # create user
        self.user = get_user_model().objects.create_user(
            username=self.username, email=self.email, password=self.password
        )
        self.user_token = Token.objects.create(user=self.user)
