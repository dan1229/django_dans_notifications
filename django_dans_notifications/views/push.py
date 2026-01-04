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

    @swagger_auto_schema(  # type: ignore[misc]
        operation_description="List push notifications for the authenticated user",
        operation_summary="List Push Notifications",
        tags=["Push Notifications"],
        manual_parameters=[
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number (default pagination: 20 items per page)",
                type=openapi.TYPE_INTEGER,
                default=1,
                required=False,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Paginated list of push notifications (default: 20 items per page)",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "count": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Total number of notifications",
                        ),
                        "next": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format=openapi.FORMAT_URI,
                            description="Next page URL",
                            nullable=True,
                        ),
                        "previous": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format=openapi.FORMAT_URI,
                            description="Previous page URL",
                            nullable=True,
                        ),
                        "results": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=NotificationPushSerializer(),
                            description="Array of push notifications for current page",
                        ),
                    },
                ),
            ),
            401: openapi.Response(description="Authentication required"),
        },
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Retrieve a paginated list of push notifications for the authenticated user.
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

    @swagger_auto_schema(  # type: ignore[misc]
        operation_description="Retrieve a specific push notification by ID",
        operation_summary="Retrieve Push Notification",
        tags=["Push Notifications"],
        manual_parameters=[
            openapi.Parameter(
                "pk",
                openapi.IN_PATH,
                description="UUID of the push notification to retrieve",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Push notification details",
                schema=NotificationPushSerializer(),
            ),
            404: openapi.Response(description="Notification not found"),
            401: openapi.Response(description="Authentication required"),
        },
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Retrieve a specific push notification by its UUID.
        Only accessible if the authenticated user is a recipient of the notification.
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

    @swagger_auto_schema(  # type: ignore[misc]
        operation_description="Create a new push notification",
        operation_summary="Create Push Notification",
        tags=["Push Notifications"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["recipients", "message"],
            properties={
                "recipients": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_STRING,
                        pattern=r"^([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|\d+)$",
                        description="Email address, UUID, or user ID",
                    ),
                    description="List of recipient emails, UUIDs, or user IDs",
                    example=[
                        "user@example.com",
                        "123e4567-e89b-12d3-a456-426614174000",
                        "123",
                    ],
                    min_items=1,
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Push notification message content",
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Push notification created successfully",
                schema=NotificationPushSerializer(),
            ),
            400: openapi.Response(description="Invalid input data"),
            401: openapi.Response(description="Authentication required"),
        },
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Create a new push notification.
        The sender is automatically set to the authenticated user's email.
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

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request_data_copy)
        if not serializer.is_valid():
            return self.response_handler.response_error(
                message="Error creating notification. Please try again later.",
                error_fields=serializer.errors,
            )
        try:
            NotificationPush.objects.create(**serializer.validated_data)
        except (ValidationError, TypeError) as e:
            return self.response_handler.response_error(
                message="Error creating notification. Please try again later.", error=e
            )

        return self.response_handler.response_success(
            results=serializer.data, status=201
        )
