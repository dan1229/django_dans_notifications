import threading
import logging

LOGGER = logging.getLogger(__name__)


#
# EmailThread
#
class EmailThread(threading.Thread):
    """
    Simple email thread to send emails asynchronously.
    Simply pass a function you want to run in a thread and any arguments.
    """

    def __init__(self, func, *args, **kwargs):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            self.func(*self.args, **self.kwargs)
        except Exception as e:
            LOGGER.error(f"Exception in EmailThread: {e}")
