from typing import Any, Dict, List, Optional, Union
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string, get_template
from django.utils import timezone
from django.utils.html import strip_tags
from smtplib import SMTPAuthenticationError, SMTPException

from .base import NotificationBase, AbstractBaseModel
from django_dans_notifications.threads import EmailThread
from django_dans_notifications.logging import LOGGER
from django.core.files import File


"""
# ==================================================================================== #
# NOTIFICATION BASIC ================================================================= #
# ==================================================================================== #
"""


#
# NOTIFICATION BASIC ==================== #
#
class NotificationBasic(NotificationBase):
    read = models.BooleanField(default=False, null=False, blank=False)
    message = models.CharField(max_length=600, null=False, blank=False)

    def __str__(self):
        return f"Basic Notification: {self.recipients}"


"""
# ==================================================================================== #
# NOTIFICATION EMAIL ================================================================= #
# ==================================================================================== #
"""


#
# NOTIFICATION EMAIL TEMPLATE MANAGER ================== #
#
class NotificationEmailTemplateManager(models.Manager):
    """
    NotificationEmailTemplateManager

    Manager for NotificationEmailTemplate.
    """

    use_in_migrations = True

    @staticmethod
    def find_email_template(template: str) -> Optional["NotificationEmailTemplate"]:
        """
        get or create NotificationEmailTemplate object for the passed 'template'

        :param str template: Path of email template to use should be of this form 'django-dans-emails/<NAME>.html'. Can also be the templates 'nickname'.
        """
        try:
            return NotificationEmailTemplate.objects.get(path=template)
        except NotificationEmailTemplate.DoesNotExist:
            pass

        # see if file exists at path 'emails/'
        try:
            return NotificationEmailTemplate.objects.get(
                path=f"django-dans-emails/{template}"
            )
        except NotificationEmailTemplate.DoesNotExist:
            pass

        # see if file exists at path 'emails/'
        try:
            return NotificationEmailTemplate.objects.get(path=f"emails/{template}")
        except NotificationEmailTemplate.DoesNotExist:
            pass

        # path doesn't exist - see if 'template' is a nickname
        try:
            email_templates = NotificationEmailTemplate.objects.filter(
                nickname=template
            )
            if email_templates.count() > 0:
                return email_templates.first()
        except NotificationEmailTemplate.DoesNotExist:
            pass

        # template not found by path or nickname - see if file exists or not
        try:
            get_template(template)
            return NotificationEmailTemplate.objects.get_or_create(
                path=template, nickname=template
            )[0]
        except TemplateDoesNotExist:
            pass

        # see if file exists at "django-dans-emails/"
        try:
            get_template(f"django-dans-emails/{template}")
            return NotificationEmailTemplate.objects.get_or_create(
                path=template, nickname=template
            )[0]
        except TemplateDoesNotExist:
            pass

        # see if file exists at "emails/"
        try:
            get_template(f"emails/{template}")
            return NotificationEmailTemplate.objects.get_or_create(
                path=template, nickname=template
            )[0]
        except TemplateDoesNotExist:
            pass

        return None


#
# NOTIFICATION EMAIL MANAGER ================== #
#
class NotificationEmailManager(models.Manager):
    """
    NotificationEmailManager

    Manager for NotificationEmail.

    Handles sending and management of objects.
    """

    use_in_migrations = True

    @staticmethod
    def send_email(
        subject: Optional[str] = f"Email from {settings.TEAM_NAME}",
        template: Optional[str] = "django-dans-emails/default.html",
        sender: Optional[str] = settings.DEFAULT_FROM_EMAIL,
        recipients: Optional[Union[str, List[str]]] = settings.DEFAULT_FROM_EMAIL,
        context: Optional[Dict[Any, Any]] = None,
        file_attachment: Optional[File] = None,
    ):
        """
        Send email function - sends email, handles notification system and object creation and everything
        WILL NOT send in test mode - set via 'IN_TEST' in settings.py file.
        """

        # check if model exists for the .html file at the given path
        # if so, ensure that an EmailTemplate objects exists for it
        # if not, error
        email_template = NotificationEmailTemplate.objects.find_email_template(
            template=template
        )
        if not email_template:
            raise ValueError("EmailTemplate with path/nickname does not exist.")

        # add TEAM_NAME var to context if appropriate
        if hasattr(settings, "TEAM_NAME") and context:
            if "team_name" not in context:
                context["team_name"] = settings.TEAM_NAME

        # render html with context object
        html_string = email_template.html_to_str(context)

        # create EmailNotification object
        notification_email = NotificationEmail.objects.create(
            template=email_template,
            subject=subject,
            context=context,
            sender=sender,
            recipients=recipients,
        )

        # create message object
        try:
            text_content = strip_tags(html_string)
            message = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=sender,
                to=notification_email.recipients_list,
            )
            message.attach_alternative(html_string, "text/html")
        except ValueError as e:
            LOGGER.error(f"Error creating email message: {type(e)} - {e}")
            notification_email.sent_successfully = False
            notification_email.save()
            return notification_email

        # attach file if applicable
        try:
            if file_attachment is not None:  # attach file if applicable
                message.attach(file_attachment.name, file_attachment.read())
                name = None
                if hasattr(file_attachment, "name"):
                    name = file_attachment.name
                LOGGER.debug(f"File attached to email: {name}")
        except AttributeError as e:
            LOGGER.error(f"Issue attaching to email: {type(e)} - {e}")

        # send email via django
        try:
            if hasattr(settings, "IN_TEST") and settings.IN_TEST:
                pass  # don't send mail in tests
            else:
                EmailThread().run(message.send, fail_silently=False)
                notification_email.sent_successfully = True
        except (
            SMTPException,
            SMTPAuthenticationError,
        ) as e:
            LOGGER.error(f"Error creating and sending email: {type(e)} - {e}")
            notification_email.sent_successfully = False

        # save regardless of status
        notification_email.datetime_sent = timezone.now()
        notification_email.save()
        return notification_email


#
# NOTIFICATION EMAIL TEMPLATE =============== #
#
class NotificationEmailTemplate(AbstractBaseModel):
    objects = NotificationEmailTemplateManager()

    path = models.CharField(max_length=300, null=False, blank=False)
    nickname = models.CharField(max_length=300, null=False, blank=False)

    def __str__(self) -> str:
        return "Email Template: " + str(self.nickname)

    def html_to_str(self, context: Dict[Any, Any]) -> str:
        try:
            return render_to_string(self.path, context)
        except TemplateDoesNotExist as e:
            LOGGER.error(f"Error rendering email template: ({type(e)}) {e}")
            return render_to_string("django-dans-emails/default.html", context)


def get_default_template():
    return NotificationEmailTemplate.objects.get_or_create(
        path="django-dans-emails/default.html"
    )[0]


#
# NOTIFICATION EMAIL =================== #
#
class NotificationEmail(NotificationBase):
    objects = NotificationEmailManager()

    template = models.ForeignKey(
        NotificationEmailTemplate,
        related_name="template",
        default=get_default_template,
        on_delete=models.DO_NOTHING,
    )
    subject = models.CharField(max_length=300, null=False, blank=False)
    context = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Notification Email: {self.sender} -> {self.recipients}"


"""
# ==================================================================================== #
# NOTIFICATION PUSH ================================================================== #
# ==================================================================================== #
"""


#
# NOTIFICATION PUSH ================== #
#
class NotificationPush(NotificationBase):
    message = models.CharField(max_length=300, null=False, blank=False)

    def __str__(self) -> str:
        return f"Notification Push: {self.recipients}"
