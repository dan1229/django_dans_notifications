import threading
import logging
from typing import Callable, Any

LOGGER = logging.getLogger(__name__)


#
# EmailThread
#
class EmailThread(threading.Thread):
    """
    Simple email thread to send emails asynchronously.
    Simply pass a function you want to run in a thread and any arguments.
    """

    def __init__(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        try:
            self.func(*self.args, **self.kwargs)
        except Exception as e:
            LOGGER.error(f"Exception in EmailThread: {e}")
