from typing import Any, Dict
from django_dans_api_toolkit.api_response_handler import ApiResponseHandler
from django.core.exceptions import ValidationError
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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

    @swagger_auto_schema(
        operation_description="List basic notifications for the authenticated user",
        operation_summary="List Basic Notifications",
        tags=['Basic Notifications'],
        responses={
            200: openapi.Response(
                description="List of basic notifications",
                schema=NotificationBasicSerializer(many=True)
            ),
            401: openapi.Response(description="Authentication required")
        }
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Retrieve a paginated list of basic notifications for the authenticated user.
        Only returns notifications where the user is a recipient.
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

    @swagger_auto_schema(
        operation_description="Retrieve a specific basic notification by ID",
        operation_summary="Retrieve Basic Notification",
        tags=['Basic Notifications'],
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="UUID of the notification to retrieve",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Basic notification details",
                schema=NotificationBasicSerializer()
            ),
            404: openapi.Response(description="Notification not found"),
            401: openapi.Response(description="Authentication required")
        }
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Retrieve a specific basic notification by its UUID.
        Only accessible if the authenticated user is a recipient of the notification.
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

    @swagger_auto_schema(
        operation_description="Create a new basic notification",
        operation_summary="Create Basic Notification",
        tags=['Basic Notifications'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['recipients', 'message'],
            properties={
                'recipients': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description="List of recipient emails or user IDs"
                ),
                'message': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Notification message content"
                )
            }
        ),
        responses={
            201: openapi.Response(
                description="Basic notification created successfully",
                schema=NotificationBasicSerializer()
            ),
            400: openapi.Response(description="Invalid input data"),
            401: openapi.Response(description="Authentication required")
        }
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Create a new basic notification.
        The sender is automatically set to the authenticated user's email.
        """
        request_data_copy: Dict[str, Any] = request.data.copy()
        if hasattr(request.user, "email"):
            request_data_copy["sender"] = (
                request.user.email
            )  # Ensure sender is included
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

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request_data_copy)
        if not serializer.is_valid():
            return self.response_handler.response_error(
                message="Error creating notification. Please try again later.",
                error_fields=serializer.errors,
            )
        try:
            NotificationBasic.objects.create(**serializer.validated_data)
        except (ValidationError, TypeError) as e:
            return self.response_handler.response_error(
                message="Error creating notification. Please try again later.", error=e
            )
        return self.response_handler.response_success(
            results=serializer.data, status=201
        )

    @swagger_auto_schema(
        operation_description="Mark a basic notification as read or unread",
        operation_summary="Update Basic Notification Read Status",
        tags=['Basic Notifications'],
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="UUID of the notification to update",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'read': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Mark notification as read (true) or unread (false)"
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Basic notification updated successfully",
                schema=NotificationBasicSerializer()
            ),
            404: openapi.Response(description="Notification not found"),
            401: openapi.Response(description="Authentication required")
        }
    )
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Update the read status of a specific basic notification.
        Only accessible if the authenticated user is a recipient of the notification.
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

        notification_basic.save()  # type: ignore[no-untyped-call]

        # serializer and return
        serializer = self.get_serializer_class()(
            notification_basic, context={"request": request}
        )
        return self.response_handler.response_success(results=serializer.data)
