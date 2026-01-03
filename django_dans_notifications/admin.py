from django.contrib import admin

from .models.notifications import (
    NotificationBasic,
    NotificationEmail,
    NotificationEmailTemplate,
    NotificationPush,
)

"""
# ==================================================================================== #
# NOTIFICATIONS ====================================================================== #
# ==================================================================================== #
"""


# ====================================================== #
# NOTIFICATION BASIC =================================== #
# ====================================================== #


class NotificationBasicAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = (
        "sender",
        "recipients",
        "read",
        "message",
        "datetime_created",
        "datetime_sent",
        "sent_successfully",
    )
    list_display_links = ("sender", "message")
    search_fields = (
        "recipients",
        "sender",
        "message",
    )
    list_filter = (
        "read",
        "sent_successfully",
        "datetime_created",
        "datetime_sent",
    )
    ordering = ("-datetime_created",)
    date_hierarchy = "datetime_created"
    list_per_page = 100


# ====================================================== #
# NOTIFICATION EMAIL =================================== #
# ====================================================== #


class NotificationEmailTemplateAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = (
        "nickname",
        "path",
        "datetime_created",
        "datetime_modified",
    )
    list_display_links = ("nickname",)
    search_fields = (
        "nickname",
        "path",
    )
    list_filter = (
        "datetime_created",
        "datetime_modified",
    )
    ordering = ("-datetime_created",)
    date_hierarchy = "datetime_created"
    list_per_page = 100


class NotificationEmailAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = (
        "sender",
        "recipients",
        "subject",
        "template",
        "datetime_created",
        "datetime_sent",
        "sent_successfully",
    )
    list_display_links = ("sender", "subject")
    search_fields = (
        "recipients",
        "sender",
        "subject",
        "template__nickname",
    )
    list_filter = (
        "sent_successfully",
        "template",
        "datetime_created",
        "datetime_sent",
    )
    ordering = ("-datetime_created",)
    date_hierarchy = "datetime_created"
    list_per_page = 100


# ====================================================== #
# NOTIFICATION PUSH ==================================== #
# ====================================================== #


class NotificationPushAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = (
        "sender",
        "recipients",
        "message",
        "datetime_created",
        "datetime_sent",
        "sent_successfully",
    )
    list_display_links = ("sender", "message")
    search_fields = (
        "recipients",
        "sender",
        "message",
    )
    list_filter = (
        "sent_successfully",
        "datetime_created",
        "datetime_sent",
    )
    ordering = ("-datetime_created",)
    date_hierarchy = "datetime_created"
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
