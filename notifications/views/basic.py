from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..helpers import str_to_bool, api_response_error, api_response_success
from ..models.basic import NotificationBasic
from ..serializers.basic import NotificationBasicSerializer

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
        return self.get_paginated_response(page)

    def retrieve(self, request, *args, **kwargs):
        """
        Endpoint to retrieve specific Basic Notification

        :param uuid pk: UUID of NotificationBasic to retrieve
        """
        pk = self.kwargs.get("pk")
        try:
            notification_basic = NotificationBasic.objects.get(pk=pk)
            if not notification_basic.recipients_contains(request.user.email):
                raise NotificationBasic.DoesNotExist
        except (NotificationBasic.DoesNotExist, ValidationError):
            return api_response_error("Notification not found.")

        # serializer and return
        serializer = self.get_serializer_class()(
            notification_basic, context={"request": request}
        )
        return api_response_success(serializer.data)

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
            return api_response_success(serializer.data)
        except (AttributeError,) as e:
            return api_response_error(e)

    def partial_update(self, request, *args, **kwargs):
        """
        Endpoint to update specific Basic Notification

        :param uuid pk: UUID of NotificationBasic to update

        :param (body, optional) bool read: mark NotificationBasic read or ont
        """
        pk = self.kwargs.get("pk")
        try:
            notification_basic = NotificationBasic.objects.get(pk=pk)
            if not notification_basic.recipients_contains(request.user.email):
                raise NotificationBasic.DoesNotExist
        except (NotificationBasic.DoesNotExist, ValidationError):
            return api_response_error("Notification not found.")

        # update object
        if request.data.get("read"):
            notification_basic.read = str_to_bool(request.data.get("read"))

        notification_basic.save()

        # serializer and return
        serializer = self.get_serializer_class()(
            notification_basic, context={"request": request}
        )
        return api_response_success(serializer.data)
