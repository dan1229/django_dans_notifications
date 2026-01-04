from typing import Any
from django_dans_api_toolkit.api_response_handler import ApiResponseHandler
from django.core.exceptions import ValidationError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..models.notifications import NotificationEmail
from ..serializers import NotificationEmailSerializer
from django.db.models import Q

"""
============================================================================================ #
EMAIL ====================================================================================== #
============================================================================================ #
"""


# =============================== #
#
# NOTIFICATION EMAIL VIEW SET
#
class NotificationEmailViewSet(viewsets.GenericViewSet):
    queryset = NotificationEmail.objects.all()
    serializer_class = NotificationEmailSerializer
    permission_classes = (IsAuthenticated,)
    response_handler = ApiResponseHandler()

    @swagger_auto_schema(
        operation_description="List email notifications for the authenticated user",
        operation_summary="List Email Notifications",
        tags=["Email Notifications"],
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
                description="Paginated list of email notifications (default: 20 items per page)",
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
                            items=NotificationEmailSerializer(),
                            description="Array of email notifications for current page",
                        ),
                    },
                ),
            ),
            401: openapi.Response(description="Authentication required"),
        },
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Retrieve a paginated list of email notifications for the authenticated user.
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
        operation_description="Retrieve a specific email notification by ID",
        operation_summary="Retrieve Email Notification",
        tags=["Email Notifications"],
        manual_parameters=[
            openapi.Parameter(
                "pk",
                openapi.IN_PATH,
                description="UUID of the email notification to retrieve",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Email notification details including rendered content",
                schema=NotificationEmailSerializer(),
            ),
            404: openapi.Response(description="Notification not found"),
            401: openapi.Response(description="Authentication required"),
        },
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Retrieve a specific email notification by its UUID.
        Returns the notification details including the rendered HTML content.
        Only accessible if the authenticated user is a recipient of the notification.
        """
        pk: str = str(self.kwargs.get("pk"))
        try:
            notification_email: NotificationEmail = NotificationEmail.objects.get(pk=pk)
            if not notification_email.recipients_contains(request.user):
                raise NotificationEmail.DoesNotExist
        except (NotificationEmail.DoesNotExist, ValidationError):
            return self.response_handler.response_error(
                message="Notification not found."
            )

        # serializer and return
        serializer = self.get_serializer_class()(
            notification_email, context={"request": request}
        )
        return self.response_handler.response_success(results=serializer.data)
