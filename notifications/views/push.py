from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import viewsets

from ..api_response_handler import ApiResponseHandler
from ..models.push import NotificationPush
from ..serializers.push import NotificationPushSerializer

"""
============================================================================================ #
PUSH ======================================================================================= #
============================================================================================ #
"""


# =============================== #
#
# NOTIFICATION PUSH VIEW SET
#
class NotificationPushViewSet(viewsets.GenericViewSet):
    response_handler = ApiResponseHandler()
    queryset = NotificationPush.objects.all()
    serializer_class = NotificationPushSerializer

    def list(self, request, *args, **kwargs):
        """
        Endpoint to list out Push Notifications
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            self.filter_queryset(
                self.queryset.filter(recipients__contains=request.user.email)
            ),
            many=True,
            context={"request": request},
        )
        page = self.paginate_queryset(serializer.data)
        return self.response_handler.response_success(
            response=self.get_paginated_response(page)
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Endpoint to retrieve specific Push Notification
        @[PARAM]
        pk          - UUID of NotificationPush to retrieve
        """
        pk = self.kwargs.get("pk")
        try:
            notification_push = NotificationPush.objects.get(pk=pk)
            if not notification_push.recipients_contains(request.user.email):
                raise NotificationPush.DoesNotExist
        except (NotificationPush.DoesNotExist, ValidationError):
            return self.response_handler.response_error(
                message="Notification not found."
            )

        # serializer and return
        serializer = self.get_serializer_class()(
            notification_push, context={"request": request}
        )
        return self.response_handler.response_success(results=serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Endpoint to create Push Notification
        """
        request_data_copy = request.data.copy()
        request_data_copy["sender"] = request.user.email
        request_data_copy["datetime_sent"] = timezone.now()
        request_data_copy["sent_successfully"] = True

        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(request_data_copy)
            NotificationPush.objects.create(**serializer.data)
        except (ValidationError, TypeError) as e:
            return self.response_handler.response_error(
                message="Error creating notification. Please try again later.", error=e
            )

        try:
            return self.response_handler.response_success(results=serializer.data)
        except (AttributeError,) as e:
            return self.response_handler.response_error(error=e)
