from django.core.exceptions import ValidationError
from rest_framework import viewsets

from api.api_response_handler import ApiResponseHandler
from notifications.models import NotificationEmail
from notifications.serializers.email import NotificationEmailSerializer

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
    response_handler = ApiResponseHandler()
    queryset = NotificationEmail.objects.all()
    serializer_class = NotificationEmailSerializer

    def list(self, request, *args, **kwargs):
        """
        Endpoint to list out Email Notifications
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
        Endpoint to retrieve specific Email Notification
        @[PARAM]
        pk          - UUID of NotificationEmail to retrieve
        """
        pk = self.kwargs.get("pk")
        try:
            notification_email = NotificationEmail.objects.get(pk=pk)
            if not notification_email.recipients_contains(request.user.email):
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
