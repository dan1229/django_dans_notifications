from django.contrib import admin

from .models.basic import NotificationBasic
from .models.email import NotificationEmail, NotificationEmailTemplate
from .models.push import NotificationPush

"""
# ==================================================================================== #
# NOTIFICATIONS ====================================================================== #
# ==================================================================================== #
"""


# ====================================================== #
# NOTIFICATION BASIC =================================== #
# ====================================================== #


class NotificationBasicAdmin(admin.ModelAdmin):
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


class NotificationEmailTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "nickname",
        "path",
    )
    list_display_links = ("nickname",)
    search_fields = (
        "nickname",
        "path",
    )
    list_per_page = 100


class NotificationEmailAdmin(admin.ModelAdmin):
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


class NotificationPushAdmin(admin.ModelAdmin):
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
