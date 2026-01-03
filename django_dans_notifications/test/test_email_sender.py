import unittest
from unittest.mock import Mock, patch, MagicMock
import time
from concurrent.futures import Future
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestEmailSender(unittest.TestCase):
    def setUp(self):
        # Mock Django settings for testing
        self.settings_patcher = patch('django_dans_notifications.email_sender.settings')
        self.mock_settings = self.settings_patcher.start()

        # Set default settings
        self.mock_settings.EMAIL_MAX_WORKERS = 3
        self.mock_settings.EMAIL_MAX_RETRIES = 3
        self.mock_settings.EMAIL_RETRY_DELAY = 0.01
        self.mock_settings.EMAIL_SYNC_MODE = True
        self.mock_settings.IN_TEST = False

        # Import after patching
        from ..email_sender import EmailSender
        # Reset singleton between tests
        EmailSender._instance = None
        EmailSender._executor = None

    def tearDown(self):
        from ..email_sender import EmailSender
        # Ensure cleanup after each test
        if EmailSender._instance and EmailSender._instance._executor:
            EmailSender._instance.shutdown(wait=False)
        EmailSender._instance = None
        self.settings_patcher.stop()

    def test_synchronous_mode(self):
        """Test that synchronous mode works correctly."""
        from ..email_sender import EmailSender

        self.mock_settings.EMAIL_SYNC_MODE = True
        sender = EmailSender()
        self.assertFalse(sender.async_enabled)

        mock_func = Mock(return_value="success")
        result = sender.send_with_retry(mock_func, "arg1", kwarg1="value1")

        mock_func.assert_called_once_with("arg1", kwarg1="value1")
        self.assertEqual(result, "success")

    def test_asynchronous_mode(self):
        """Test that asynchronous mode returns a Future."""
        from ..email_sender import EmailSender

        self.mock_settings.EMAIL_SYNC_MODE = False
        self.mock_settings.EMAIL_MAX_WORKERS = 2

        sender = EmailSender()
        self.assertTrue(sender.async_enabled)
        self.assertEqual(sender.max_workers, 2)

        mock_func = Mock(return_value="async_success")
        future = sender.send_with_retry(mock_func, "arg1")

        self.assertIsInstance(future, Future)
        # Wait for completion
        result = future.result(timeout=1)
        mock_func.assert_called_once_with("arg1")
        self.assertEqual(result, "async_success")

    def test_retry_logic_success_on_second_attempt(self):
        """Test that retry logic works when function succeeds on second attempt."""
        from ..email_sender import EmailSender

        self.mock_settings.EMAIL_SYNC_MODE = True
        self.mock_settings.EMAIL_MAX_RETRIES = 3
        self.mock_settings.EMAIL_RETRY_DELAY = 0.01

        sender = EmailSender()
        mock_func = Mock(side_effect=[Exception("First attempt fails"), "success"])

        result = sender.send_with_retry(mock_func)

        self.assertEqual(mock_func.call_count, 2)
        self.assertEqual(result, "success")

    def test_retry_logic_all_attempts_fail(self):
        """Test that exception is raised after all retries fail."""
        from ..email_sender import EmailSender

        self.mock_settings.EMAIL_SYNC_MODE = True
        self.mock_settings.EMAIL_MAX_RETRIES = 3
        self.mock_settings.EMAIL_RETRY_DELAY = 0.01

        sender = EmailSender()
        mock_func = Mock(side_effect=Exception("Always fails"))

        with self.assertRaises(Exception) as context:
            sender.send_with_retry(mock_func)

        self.assertEqual(mock_func.call_count, 3)
        self.assertEqual(str(context.exception), "Always fails")

    def test_retry_with_different_exceptions(self):
        """Test retry logic with different exception types."""
        from ..email_sender import EmailSender

        self.mock_settings.EMAIL_SYNC_MODE = True
        self.mock_settings.EMAIL_MAX_RETRIES = 3

        sender = EmailSender()
        exceptions = [
            ValueError("First error"),
            TypeError("Second error"),
            RuntimeError("Final error")
        ]
        mock_func = Mock(side_effect=exceptions)

        with self.assertRaises(RuntimeError) as context:
            sender.send_with_retry(mock_func)

        self.assertEqual(mock_func.call_count, 3)
        self.assertEqual(str(context.exception), "Final error")

    def test_test_mode_disables_async(self):
        """Test that IN_TEST setting disables async mode."""
        from ..email_sender import EmailSender

        self.mock_settings.IN_TEST = True
        self.mock_settings.EMAIL_SYNC_MODE = False

        sender = EmailSender()
        self.assertFalse(sender.async_enabled)

    def test_singleton_pattern(self):
        """Test that EmailSender follows singleton pattern."""
        from ..email_sender import EmailSender

        sender1 = EmailSender()
        sender2 = EmailSender()
        self.assertIs(sender1, sender2)

    def test_shutdown(self):
        """Test graceful shutdown of thread pool."""
        from ..email_sender import EmailSender

        self.mock_settings.EMAIL_SYNC_MODE = False

        sender = EmailSender()
        self.assertTrue(sender.async_enabled)
        self.assertIsNotNone(sender._executor)

        sender.shutdown()
        self.assertIsNone(sender._executor)

    def test_get_stats_sync_mode(self):
        """Test stats in synchronous mode."""
        from ..email_sender import EmailSender

        self.mock_settings.EMAIL_SYNC_MODE = True

        sender = EmailSender()
        stats = sender.get_stats()

        self.assertEqual(stats['async_enabled'], False)
        self.assertEqual(stats['pending_tasks'], 0)

    def test_get_stats_async_mode(self):
        """Test stats in asynchronous mode."""
        from ..email_sender import EmailSender

        self.mock_settings.EMAIL_SYNC_MODE = False
        self.mock_settings.EMAIL_MAX_WORKERS = 5

        sender = EmailSender()
        stats = sender.get_stats()

        self.assertEqual(stats['async_enabled'], True)
        self.assertEqual(stats['max_workers'], 5)

    def test_send_email_async_convenience_function(self):
        """Test the convenience function for backward compatibility."""
        from ..email_sender import send_email_async

        self.mock_settings.EMAIL_SYNC_MODE = True

        mock_func = Mock(return_value="convenience_result")
        result = send_email_async(mock_func, "arg1", kwarg1="value1")

        mock_func.assert_called_once_with("arg1", kwarg1="value1")
        self.assertEqual(result, "convenience_result")

    def test_multiple_async_sends(self):
        """Test that multiple async sends work correctly."""
        from ..email_sender import EmailSender

        self.mock_settings.EMAIL_SYNC_MODE = False
        self.mock_settings.EMAIL_MAX_WORKERS = 1

        sender = EmailSender()
        results = []
        mock_func = Mock(return_value="async_result")

        for i in range(3):
            future = sender.send_with_retry(mock_func, f"arg{i}")
            results.append(future)

        # Wait for all futures to complete
        for i, future in enumerate(results):
            result = future.result(timeout=2)
            self.assertEqual(result, "async_result")

        self.assertEqual(mock_func.call_count, 3)

    def test_exponential_backoff(self):
        """Test that exponential backoff is applied between retries."""
        from ..email_sender import EmailSender

        self.mock_settings.EMAIL_SYNC_MODE = True
        self.mock_settings.EMAIL_RETRY_DELAY = 0.01

        sender = EmailSender()

        # Track time between calls
        call_times = []

        def track_time(*args, **kwargs):
            call_times.append(time.time())
            if len(call_times) < 3:
                raise Exception("Fail")
            return "success"

        mock_func = Mock(side_effect=track_time)
        result = sender.send_with_retry(mock_func)

        self.assertEqual(result, "success")
        self.assertEqual(len(call_times), 3)

        # Check that delays increase (exponential backoff)
        # First retry: 0.01 seconds
        # Second retry: 0.02 seconds (0.01 * 2)
        delay1 = call_times[1] - call_times[0]
        delay2 = call_times[2] - call_times[1]

        # Allow some tolerance for timing
        self.assertGreater(delay2, delay1)


if __name__ == "__main__":
    unittest.main()