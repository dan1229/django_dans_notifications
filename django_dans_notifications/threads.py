from threading import Thread


#
# EmailThread
#
class EmailThread(Thread):
    """
    Simple email thread to send emails asynchronously.
    Simply pass a function you want to run in a thread and any arguments
    """

    def run(self, func, *args):
        func(*args)
