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

    def setUp(self) -> None:
        super(APITestCase, self).setUp()

        # store standard api factory
        self.factory = APIRequestFactory()

        # create user
        if hasattr(get_user_model().objects, "create_user"):
            # if user model has create_user method, use it
            self.user = get_user_model().objects.create_user(  # type: ignore[attr-defined]
                username=self.username, email=self.email, password=self.password
            )
        else:
            # otherwise, use create method
            self.user = get_user_model().objects.create(
                username=self.username, email=self.email, password=self.password
            )
        self.user_token = Token.objects.create(user=self.user)
