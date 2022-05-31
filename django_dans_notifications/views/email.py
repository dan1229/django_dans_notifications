from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..helpers import api_response_success, api_response_error
from ..models.email import NotificationEmail
from ..serializers.email import NotificationEmailSerializer

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
        return self.get_paginated_response(page)

    def retrieve(self, request, *args, **kwargs):
        """
        Endpoint to retrieve specific Email Notification

        :param uuid pk: UUID of NotificationEmail to retrieve
        """
        pk = self.kwargs.get("pk")
        try:
            notification_email = NotificationEmail.objects.get(pk=pk)
            if not notification_email.recipients_contains(request.user.email):
                raise NotificationEmail.DoesNotExist
        except (NotificationEmail.DoesNotExist, ValidationError):
            return api_response_error("Notification not found.")

        # serializer and return
        serializer = self.get_serializer_class()(
            notification_email, context={"request": request}
        )
        return api_response_success(serializer.data)
