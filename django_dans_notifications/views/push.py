from typing import Any, Dict
from django_dans_api_toolkit.api_response_handler import ApiResponseHandler
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..models.notifications import NotificationPush
from ..serializers import NotificationPushSerializer
from django.db.models import Q

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
    queryset = NotificationPush.objects.all()
    serializer_class = NotificationPushSerializer
    permission_classes = (IsAuthenticated,)
    response_handler = ApiResponseHandler()

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Endpoint to list out Push Notifications
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            self.filter_queryset(
                self.queryset.filter(
                    Q(recipients__contains=request.user.email)  # type: ignore[union-attr]
                    | Q(recipients__contains=request.user.id)  # type: ignore[union-attr]
                )
            ),
            many=True,
            context={"request": request},
        )
        page = self.paginate_queryset(serializer.data)
        return self.response_handler.response_success(
            response=self.get_paginated_response(page)
        )

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Endpoint to retrieve specific Push Notification

        :param uuid pk: UUID of NotificationPush to retrieve
        """
        pk: str = str(self.kwargs.get("pk"))
        try:
            notification_push: NotificationPush = NotificationPush.objects.get(pk=pk)
            if not notification_push.recipients_contains(request.user):
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

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Endpoint to create Push Notification
        """
        request_data_copy: Dict[str, Any] = request.data.copy()
        if hasattr(request.user, "email"):
            request_data_copy["sender"] = request.user.email
        else:
            return self.response_handler.response_error(
                message="User email required to send notification."
            )
        request_data_copy["datetime_sent"] = timezone.now()
        request_data_copy["sent_successfully"] = True

        # Check for required fields
        if not request_data_copy.get("recipients"):
            return self.response_handler.response_error(message="Recipients required.")
        if not request_data_copy.get("message"):
            return self.response_handler.response_error(message="Message required.")

        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(request_data_copy)
            NotificationPush.objects.create(**serializer.data)
        except (ValidationError, TypeError) as e:
            return self.response_handler.response_error(
                message="Error creating notification. Please try again later.", error=e
            )

        return self.response_handler.response_success(
            results=serializer.data, status=201
        )
