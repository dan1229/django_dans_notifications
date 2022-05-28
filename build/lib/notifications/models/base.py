from django.db import models
from safedelete import SOFT_DELETE_CASCADE

from core.models.base import AbstractBaseModel

"""
# ==================================================================================== #
# NOTIFICATION BASE ================================================================== #
# ==================================================================================== #
"""


#
# NOTIFICATION BASE =================== #
#
class NotificationBase(AbstractBaseModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    datetime_sent = models.DateTimeField(null=True, blank=True)
    sent_successfully = models.BooleanField(default=False, null=False, blank=False)
    sender = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        help_text="This should be the users email.",
    )
    recipients = models.CharField(
        max_length=900,
        null=False,
        blank=False,
        help_text="Comma separated list of email recipients.",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return "Notification Base"

    def save(self, keep_deleted=False, **kwargs):
        # cleanup 'recipients'
        self.recipients = self.recipients_cleanup()
        return super(NotificationBase, self).save(**kwargs)

    @property
    def recipients_list(self):
        return self.recipients.split(",")

    def recipients_cleanup(self):
        # take in whatever is currently set as recipients
        list_recipients = self.recipients

        # if a str or conversion of a list, convert to a list of the recipients
        if "," in list_recipients or "[" in list_recipients or "]" in list_recipients:
            tmp = (
                str(self.recipients).replace("[", "").replace("]", "").replace(" ", "")
            )
            list_recipients = tmp.split(",")

        # if the last element is empty, remove it
        if len(list_recipients) > 0:
            if list_recipients[len(list_recipients) - 1] == "":
                list_recipients.pop()

        # if a list, convert standardize as str 'recp1,recp2,recp3'
        if type(list_recipients) == list:
            res = ",".join(str(e) for e in list_recipients)
        else:  # probably a string, just return as is
            res = list_recipients

        # remove any extra chars
        res = res.replace("'", "").replace('"', "")
        return res

    def recipients_contains(self, user):
        """
        Detect if 'user' is involved with this notification or not
        """
        if str(user) in self.recipients:
            return True
        return False
