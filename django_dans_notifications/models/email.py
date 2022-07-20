import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string, get_template
from django.utils import timezone
from django.utils.html import strip_tags
from smtplib import SMTPException

from .base import NotificationBase, AbstractBaseModel

logger = logging.getLogger(__name__)

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
    def find_email_template(template):
        """
        get or create NotificationEmailTemplate object for the passed 'template'

        :param str template: Path of email template to use should be of this form 'emails/<NAME>.html'. Can also be the templates 'nickname'.
        """
        try:
            return NotificationEmailTemplate.objects.get(path=template)
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
            tmp = get_template(template)
            return NotificationEmailTemplate.objects.get_or_create(
                path=template, nickname=template
            )[0]
        except TemplateDoesNotExist:
            pass

        # see if file exists at "emails/"
        try:
            tmp = get_template(f"emails/{template}")
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
        subject="Email from Dan's Backend",
        template="emails/default.html",
        sender=settings.DEFAULT_FROM_EMAIL,
        recipients=None,
        context=None,
    ):
        """
        Send email function - sends email, handles notification system and object creation and everything
        WILL NOT send in test mode - set via 'IN_TEST' in settings.py file.

        :param str subject: Subject for email.
        :param str template: Template file path or nickname.
        :param str sender: From email.
        :param str recipients: List of email(s) to send to.
        :param dict context: Context dict for template.
        """
        if recipients is None:
            recipients = ""

        # check if model exists for the .html file at the given path
        # if so, ensure that an EmailTemplate objects exists for it
        # if not, error
        email_template = NotificationEmailTemplate.objects.find_email_template(
            template=template
        )
        if not email_template:
            raise ValueError("EmailTemplate with path/nickname does not exist.")

        # add TEAM_NAME var to context if appropriate
        if hasattr(settings.TEAM_NAME) and context:
            if not "team_name" in context:
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

        # send email via django
        try:
            text_content = strip_tags(html_string)
            message = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=sender,
                to=notification_email.recipients_list,
            )
            message.attach_alternative(html_string, "text/html")
            if hasattr(settings, "IN_TEST") and not settings.IN_TEST:
                pass  # dont send mail in tests
            else:
                message.send(fail_silently=False)
            notification_email.sent_successfully = True
        except SMTPException as e:
            logger.error(e)
            notification_email.sent_successfully = False
        notification_email.sent_datetime = timezone.now()  # save regardless of status
        notification_email.save()
        return notification_email


#
# NOTIFICATION EMAIL TEMPLATE =============== #
#
class NotificationEmailTemplate(AbstractBaseModel):
    objects = NotificationEmailTemplateManager()

    path = models.CharField(max_length=300, null=False, blank=False)
    nickname = models.CharField(max_length=300, null=False, blank=False)

    def __str__(self):
        return "Email Template: " + str(self.nickname)

    def html_to_str(self, context):
        try:
            return render_to_string(self.path, context)
        except Exception as e:
            logger.error(e)
            return render_to_string("emails/default.html", context)


def get_default_template():
    return NotificationEmailTemplate.objects.get_or_create(path="emails/default.html")[
        0
    ]


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

    def __str__(self):
        return f"Notification Email: {self.sender} -> {self.recipients}"
