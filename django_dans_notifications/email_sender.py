import logging
import time
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable, Any, Optional, Dict
import atexit
from django.conf import settings

LOGGER = logging.getLogger(__name__)


class EmailSender:
    """
    Improved email sender using ThreadPoolExecutor for better thread management.

    Features:
    - Controlled concurrency with max workers
    - Retry logic for failed sends
    - Graceful shutdown
    - Better error tracking
    - Optional synchronous mode for testing
    """

    _instance: Optional["EmailSender"] = None
    _executor: Optional[ThreadPoolExecutor] = None
    _initialized: bool = False

    def __new__(cls) -> "EmailSender":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized") and self._initialized:
            return

        self._initialized = True
        # Use getattr with defaults - fully backward compatible
        self.max_workers = getattr(settings, "EMAIL_MAX_WORKERS", 3)
        self.max_retries = getattr(settings, "EMAIL_MAX_RETRIES", 3)
        self.retry_delay = getattr(settings, "EMAIL_RETRY_DELAY", 1.0)

        # Use synchronous mode in tests or when explicitly configured
        self.async_enabled = not getattr(settings, "EMAIL_SYNC_MODE", False)
        if getattr(settings, "IN_TEST", False):
            self.async_enabled = False

        if self.async_enabled:
            self._executor = ThreadPoolExecutor(
                max_workers=self.max_workers, thread_name_prefix="email_sender"
            )
            # Register cleanup on exit
            atexit.register(self.shutdown)

        LOGGER.info(
            f"EmailSender initialized: async={self.async_enabled}, "
            f"max_workers={self.max_workers}, max_retries={self.max_retries}"
        )

    def send_with_retry(
        self, func: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> Optional[Future[Any]]:
        """
        Send email with retry logic.

        Returns:
            - Future object if async (can be used to check status)
            - None if synchronous
        """
        if not self.async_enabled:
            # Synchronous mode for testing
            self._execute_with_retry(func, *args, **kwargs)
            return None

        # Async mode
        if self._executor is None:
            LOGGER.error("Executor not initialized but async mode is enabled")
            return None

        future = self._executor.submit(self._execute_with_retry, func, *args, **kwargs)

        # Add callback for logging
        future.add_done_callback(self._log_completion)

        return future

    def _execute_with_retry(
        self, func: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> Any:
        """Execute function with retry logic."""
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                result = func(*args, **kwargs)
                if attempt > 0:
                    LOGGER.info(f"Email sent successfully after {attempt + 1} attempts")
                return result

            except Exception as e:
                last_exception = e
                LOGGER.warning(
                    f"Email send attempt {attempt + 1}/{self.max_retries} failed: {e}"
                )

                if attempt < self.max_retries - 1:
                    # Exponential backoff
                    sleep_time = self.retry_delay * (2**attempt)
                    time.sleep(sleep_time)

        # All retries failed
        LOGGER.error(
            f"Email send failed after {self.max_retries} attempts: {last_exception}"
        )
        if last_exception is not None:
            raise last_exception
        raise Exception("Email send failed with unknown error")

    def _log_completion(self, future: Future[Any]) -> None:
        """Log completion of async email send."""
        try:
            future.result()  # This will raise if there was an exception
        except Exception as e:
            LOGGER.error(f"Async email send failed: {e}")

    def shutdown(self, wait: bool = True) -> None:
        """
        Gracefully shutdown the thread pool.

        Args:
            wait: If True, wait for all pending tasks to complete
        """
        if self._executor is not None:
            LOGGER.info("Shutting down email sender thread pool")
            self._executor.shutdown(wait=wait)
            self._executor = None

    def get_stats(self) -> Dict[str, Any]:
        """Get current stats about the email sender."""
        if not self.async_enabled or self._executor is None:
            return {
                "async_enabled": self.async_enabled,
                "pending_tasks": 0,
                "max_workers": self.max_workers,
            }

        # ThreadPoolExecutor doesn't expose queue size directly,
        # but we can track this if needed by wrapping submit()
        return {
            "async_enabled": self.async_enabled,
            "max_workers": self.max_workers,
            "max_retries": self.max_retries,
        }


# Convenience function for backward compatibility
def send_email_async(
    func: Callable[..., Any], *args: Any, **kwargs: Any
) -> Optional[Future[Any]]:
    """
    Send email asynchronously using the singleton EmailSender.

    This provides a simple interface that's backward compatible with
    the old EmailThread usage.
    """
    sender = EmailSender()
    return sender.send_with_retry(func, *args, **kwargs)
