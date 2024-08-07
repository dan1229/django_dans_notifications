from typing import Any, List
import uuid

from django.db import models

"""
# ==================================================================================== #
# ABSTRACT BASE MODEL ================================================================ #
# ==================================================================================== #
"""


class AbstractBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # type: ignore[var-annotated]

    datetime_created = models.DateTimeField(auto_now_add=True, editable=False)  # type: ignore[var-annotated]
    datetime_modified = models.DateTimeField(auto_now=True)  # type: ignore[var-annotated]

    class Meta:
        abstract = True
        ordering = ["datetime_created"]

    def __str__(self) -> str:
        return "Abstract Base Model"


"""
# ==================================================================================== #
# NOTIFICATION BASE ================================================================== #
# ==================================================================================== #
"""


#
# NOTIFICATION BASE =================== #
#
class NotificationBase(AbstractBaseModel):
    datetime_sent = models.DateTimeField(null=True, blank=True)  # type: ignore[var-annotated]
    sent_successfully = models.BooleanField(default=False, null=False, blank=False)  # type: ignore[var-annotated]
    sender = models.CharField(  # type: ignore[var-annotated]
        max_length=300,
        null=False,
        blank=False,
        help_text="This should be the sending users email.",
    )
    recipients = models.CharField(  # type: ignore[var-annotated]
        max_length=900,
        null=False,
        blank=False,
        help_text="Comma separated list of email recipients.",
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return "Notification Base"

    def save(self, **kwargs):  # type: ignore
        # cleanup 'recipients'
        self.recipients = self.recipients_cleanup()
        return super(NotificationBase, self).save(**kwargs)

    @property
    def recipients_list(self) -> List[Any]:
        return self.recipients.split(",")  # type: ignore[no-any-return]

    def recipients_cleanup(self) -> str:
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
        if isinstance(list_recipients, list):
            res = ",".join(str(e) for e in list_recipients)
        else:  # probably a string, just return as is
            res = list_recipients

        # remove any extra chars
        res = res.replace("'", "").replace('"', "")
        return res

    def recipients_contains(self, user: Any) -> bool:
        """
        Detect if 'user' is involved with this notification or not
        """
        if isinstance(user, str):
            if user in self.recipients:
                return True
        else:
            if hasattr(user, "email") and str(user.email) in self.recipients:
                return True
            if hasattr(user, "id") and str(user.id) in self.recipients:
                return True
        return False
