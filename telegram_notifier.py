"""
Telegram Bot API integration for sending notifications.

Handles message sending with comprehensive error handling and retry logic.
"""

import logging
import time
from typing import Final

import requests

logger = logging.getLogger(__name__)

# Constants
DEFAULT_TIMEOUT: Final = 10
DEFAULT_MAX_RETRIES: Final = 3
BASE_API_URL: Final = "https://api.telegram.org/bot"
PARSE_MODE: Final = "HTML"

# HTTP status codes
STATUS_RATE_LIMITED = 429
STATUS_UNAUTHORIZED = 401
STATUS_BAD_REQUEST = 400

# Default retry-after delay for rate limiting (seconds)
DEFAULT_RETRY_AFTER: Final = 5


class TelegramNotifier:
    """Handles sending messages to Telegram Bot API."""

    def __init__(self, bot_token: str, chat_id: str) -> None:
        """
        Initialize Telegram notifier.

        Args:
            bot_token: Telegram bot authentication token.
            chat_id: Telegram chat ID to send messages to.

        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"{BASE_API_URL}{bot_token}/sendMessage"

    def send_message(self, message: str, max_retries: int = DEFAULT_MAX_RETRIES) -> bool:
        """
        Send a message to Telegram with retry logic.

        Implements exponential backoff for retries and handles various
        error conditions including rate limiting, authentication errors,
        and network issues.

        Args:
            message: Message text to send.
            max_retries: Maximum number of retry attempts (default: 3).

        Returns:
            True if message sent successfully, False otherwise.

        """
        for attempt in range(max_retries):
            try:
                success = self._send_request(message)
                if success:
                    return True
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1}/{max_retries}")
            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error on attempt {attempt + 1}/{max_retries}")
            except requests.exceptions.HTTPError as e:
                should_continue = self._handle_http_error(e, attempt, max_retries)
                if not should_continue:
                    return False
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error on attempt {attempt + 1}/{max_retries}: {e}")

            self._wait_before_retry(attempt, max_retries)

        logger.error(f"Failed to send message after {max_retries} attempts")
        return False

    def _send_request(self, message: str) -> bool:
        """Send a single HTTP request to Telegram API."""
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": PARSE_MODE
        }

        response = requests.post(self.api_url, json=payload, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()

        result = response.json()
        if result.get("ok"):
            preview = message[:50] + "..." if len(message) > 50 else message
            logger.info(f"Message sent successfully: {preview}")
            return True

        description = result.get("description", "Unknown error")
        logger.error(f"Telegram API error: {description}")
        return False

    def _handle_http_error(
        self, error: requests.exceptions.HTTPError, attempt: int, max_retries: int
    ) -> bool:
        """
        Handle HTTP errors with specific logic for common status codes.

        Returns:
            False if the error is fatal and should not retry,
            True if the request should continue/retry.

        """
        status_code = error.response.status_code

        if status_code == STATUS_RATE_LIMITED:
            retry_after = error.response.headers.get("Retry-After", DEFAULT_RETRY_AFTER)
            logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
            time.sleep(int(retry_after))
            return True

        if status_code == STATUS_UNAUTHORIZED:
            logger.error("Invalid bot token. Please check TELEGRAM_BOT_TOKEN.")
            return False

        if status_code == STATUS_BAD_REQUEST:
            logger.error("Invalid chat ID or message format. Please check TELEGRAM_CHAT_ID.")
            return False

        logger.error(f"HTTP error: {error}")
        return attempt < max_retries - 1

    def _wait_before_retry(self, attempt: int, max_retries: int) -> None:
        """Wait with exponential backoff before retrying."""
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt
            logger.info(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

    def test_connection(self) -> bool:
        """
        Test the connection to Telegram API.

        Returns:
            True if connection successful, False otherwise.

        """
        return self.send_message("🧪 Test message - Water Reminder Bot is active!")
