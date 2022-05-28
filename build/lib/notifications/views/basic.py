from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import viewsets

from api.api_response_handler import ApiResponseHandler
from core.helpers import str_to_bool
from notifications.models import NotificationBasic
from notifications.serializers.basic import NotificationBasicSerializer

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
    response_handler = ApiResponseHandler()
    queryset = NotificationBasic.objects.all()
    serializer_class = NotificationBasicSerializer

    def list(self, request, *args, **kwargs):
        """
        Endpoint to list out Basic Notifications
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
        Endpoint to retrieve specific Basic Notification
        @[PARAM]
        pk          - UUID of NotificationBasic to retrieve
        """
        pk = self.kwargs.get("pk")
        try:
            notification_basic = NotificationBasic.objects.get(pk=pk)
            if not notification_basic.recipients_contains(request.user.email):
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

    def create(self, request, *args, **kwargs):
        """
        Endpoint to create Basic Notification
        """
        request_data_copy = request.data.copy()
        request_data_copy["sender"] = request.user.email
        request_data_copy["datetime_sent"] = timezone.now()
        request_data_copy["sent_successfully"] = True

        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(request_data_copy)
            NotificationBasic.objects.create(**serializer.data)
        except (ValidationError, TypeError) as e:
            return self.response_handler.response_error(
                message="Error creating notification. Please try again later.", error=e
            )

        try:
            return self.response_handler.response_success(results=serializer.data)
        except (AttributeError,) as e:
            return self.response_handler.response_error(error=e)

    def partial_update(self, request, *args, **kwargs):
        """
        Endpoint to update specific Basic Notification
        @[PARAM]
        pk          - UUID of NotificationBasic to update
        """
        pk = self.kwargs.get("pk")
        try:
            notification_basic = NotificationBasic.objects.get(pk=pk)
            if not notification_basic.recipients_contains(request.user.email):
                raise NotificationBasic.DoesNotExist
        except (NotificationBasic.DoesNotExist, ValidationError):
            return self.response_handler.response_error(
                message="Notification not found."
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
