from typing import Any
from django_dans_api_toolkit.api_response_handler import ApiResponseHandler
from django.core.exceptions import ValidationError
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

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Endpoint to list out Email Notifications
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
        Endpoint to retrieve specific Email Notification

        :param uuid pk: UUID of NotificationEmail to retrieve
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
