from typing import Any, List
import uuid

from django.db import models
from django.db.models import Q

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


def recipient_q(value: Any, field: str = "recipients") -> Q:
    """
    Match rows whose comma-joined `field` holds `value` as one whole entry.

    A plain `__contains` is a substring match, so `ob@example.com` would match a
    row sent to `bob@example.com` - and hand its reader that row's magic-link or
    password-reset URL. `recipients_cleanup()` stores entries as `a,b,c` with no
    spaces, so one entry is the whole string, the first, the last or a middle one.
    """
    entry = str(value or "")
    if not entry:
        return Q(pk__in=[])
    return (
        Q(**{f"{field}__iexact": entry})
        | Q(**{f"{field}__istartswith": f"{entry},"})
        | Q(**{f"{field}__iendswith": f",{entry}"})
        | Q(**{f"{field}__icontains": f",{entry},"})
    )


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
        Detect if 'user' is involved with this notification or not.

        Whole-entry match only, never a substring - see `recipient_q`.
        """
        candidates: List[Any]
        if isinstance(user, str):
            candidates = [user]
        else:
            candidates = [getattr(user, "email", None), getattr(user, "id", None)]
        entries = {e.strip().lower() for e in self.recipients_list if e.strip()}
        return any(
            str(c).strip().lower() in entries
            for c in candidates
            if c and str(c).strip()
        )
