import unittest
from unittest.mock import Mock
from ..logging import LOGGER
from ..threads import EmailThread


class TestEmailThread(unittest.TestCase):
    def test_email_thread_executes_function(self):
        mock_func = Mock()
        thread = EmailThread(mock_func)
        thread.start()
        thread.join()  # Wait for the thread to finish
        mock_func.assert_called_once()

    def test_email_thread_passes_arguments(self):
        mock_func = Mock()
        args = (1, 2, 3)
        kwargs = {"a": "b", "c": "d"}
        thread = EmailThread(mock_func, *args, **kwargs)
        thread.start()
        thread.join()  # Wait for the thread to finish
        mock_func.assert_called_once_with(*args, **kwargs)

    def test_email_thread_handles_exception(self):
        def func_that_raises():
            raise ValueError("Test exception")

        thread = EmailThread(func_that_raises)

        with self.assertLogs(LOGGER, level="ERROR") as log:
            thread.start()
            thread.join()  # Wait for the thread to finish
            self.assertTrue(
                any(
                    "Exception in EmailThread: Test exception" in message
                    for message in log.output
                )
            )


if __name__ == "__main__":
    unittest.main()
