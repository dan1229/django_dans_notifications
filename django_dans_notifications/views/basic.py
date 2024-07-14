from typing import Any, Dict
from django_dans_api_toolkit.api_response_handler import ApiResponseHandler
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..helpers import str_to_bool
from ..models.notifications import NotificationBasic
from ..serializers import NotificationBasicSerializer
from django.db.models import Q

"""
============================================================================================ #
BASIC ====================================================================================== #
============================================================================================ #
"""


# =============================== #
#
# NOTIFICATION BASIC VIEW SET
#
class NotificationBasicViewSet(viewsets.GenericViewSet):
    queryset = NotificationBasic.objects.all()
    serializer_class = NotificationBasicSerializer
    permission_classes = (IsAuthenticated,)
    response_handler = ApiResponseHandler()

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Endpoint to list out Basic Notifications
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
        Endpoint to retrieve specific Basic Notification

        :param uuid pk: UUID of NotificationBasic to retrieve
        """
        pk: str = str(self.kwargs.get("pk"))
        try:
            notification_basic: NotificationBasic = NotificationBasic.objects.get(pk=pk)
            if not notification_basic.recipients_contains(request.user):
                raise NotificationBasic.DoesNotExist
        except (NotificationBasic.DoesNotExist, ValidationError):
            return self.response_handler.response_error(
                message="Notification not found."
            )

        # serializer and return
        serializer = self.get_serializer_class()(
            notification_basic, context={"request": request}
        )
        return self.response_handler.response_success(results=serializer.data)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Endpoint to create Basic Notification
        """
        request_data_copy: Dict[str, Any] = request.data.copy()
        if hasattr(request.user, "email"):
            request_data_copy["recipients"] = request.user.email
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
            NotificationBasic.objects.create(**serializer.data)
        except (ValidationError, TypeError) as e:
            return self.response_handler.response_error(
                message="Error creating notification. Please try again later.", error=e
            )

        try:
            return self.response_handler.response_success(
                results=serializer.data, status=201
            )
        except AttributeError as e:
            return self.response_handler.response_error(
                message="Error creating notification. Please try again later.", error=e
            )

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Endpoint to update specific Basic Notification

        :param uuid pk: UUID of NotificationBasic to update

        :param (body, optional) bool read: mark NotificationBasic read or not
        """
        pk: str = str(self.kwargs.get("pk"))
        try:
            notification_basic: NotificationBasic = NotificationBasic.objects.get(pk=pk)
            if not notification_basic.recipients_contains(request.user):
                raise NotificationBasic.DoesNotExist
        except (NotificationBasic.DoesNotExist, ValidationError) as e:
            return self.response_handler.response_error(
                message="Notification not found.", error=e
            )

        # update object
        if request.data.get("read"):
            notification_basic.read = str_to_bool(request.data.get("read"))

        notification_basic.save()

        # serializer and return
        serializer = self.get_serializer_class()(
            notification_basic, context={"request": request}
        )
        return self.response_handler.response_success(results=serializer.data)
