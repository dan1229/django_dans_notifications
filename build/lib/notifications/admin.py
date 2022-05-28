from django.contrib import admin
from safedelete.admin import SafeDeleteAdmin, highlight_deleted

from notifications.models import *

"""
# ==================================================================================== #
# NOTIFICATIONS ====================================================================== #
# ==================================================================================== #
"""


# ====================================================== #
# NOTIFICATION BASIC =================================== #
# ====================================================== #


class NotificationBasicAdmin(SafeDeleteAdmin):
    list_display = (
        highlight_deleted,
        "sender",
        "recipients",
        "read",
        "message",
        "datetime_sent",
        "sent_successfully",
    ) + SafeDeleteAdmin.list_display
    list_display_links = ("sender", "message")
    search_fields = (
        "datetime_sent",
        "sent_successfully",
        "recipients",
        "sender",
        "message",
    )
    list_per_page = 100


# ====================================================== #
# NOTIFICATION EMAIL =================================== #
# ====================================================== #


class NotificationEmailTemplateAdmin(SafeDeleteAdmin):
    list_display = (
        highlight_deleted,
        "nickname",
        "path",
    ) + SafeDeleteAdmin.list_display
    list_display_links = ("nickname",)
    search_fields = (
        "nickname",
        "path",
    )
    list_per_page = 100


class NotificationEmailAdmin(SafeDeleteAdmin):
    list_display = (
        highlight_deleted,
        "sender",
        "recipients",
        "subject",
        "template",
        "datetime_sent",
        "sent_successfully",
    ) + SafeDeleteAdmin.list_display
    list_display_links = ("sender", "subject")
    search_fields = (
        "datetime_sent",
        "sent_successfully",
        "recipients",
        "sender",
        "template",
    )
    list_per_page = 100


# ====================================================== #
# NOTIFICATION PUSH ==================================== #
# ====================================================== #


class NotificationPushAdmin(SafeDeleteAdmin):
    list_display = (
        highlight_deleted,
        "sender",
        "recipients",
        "message",
        "datetime_sent",
        "sent_successfully",
    ) + SafeDeleteAdmin.list_display
    list_display_links = ("sender", "message")
    search_fields = (
        "datetime_sent",
        "sent_successfully",
        "recipients",
        "sender",
        "message",
    )
    list_per_page = 100


"""
# ==================================================================================== #
# REGISTER =========================================================================== #
# ==================================================================================== #
"""

admin.site.register(NotificationBasic, NotificationBasicAdmin)
admin.site.register(NotificationEmailTemplate, NotificationEmailTemplateAdmin)
admin.site.register(NotificationEmail, NotificationEmailAdmin)
admin.site.register(NotificationPush, NotificationPushAdmin)
