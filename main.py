"""
Water Drinking Reminder System.

Main application entry point that orchestrates configuration,
Telegram notifications, and scheduling.
"""

import logging
import signal
import sys
import time
from typing import Final

from config import Config
from telegram_notifier import TelegramNotifier
from scheduler import WaterReminderScheduler

# Constants
LOG_FILE: Final = "logs/app.log"
LOG_FORMAT: Final = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL: Final = logging.INFO
MAIN_LOOP_INTERVAL: Final = 60  # seconds
SEPARATOR_LENGTH: Final = 60

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class WaterReminderApp:
    """Main application class for the water reminder system."""

    def __init__(self) -> None:
        """Initialize the application with signal handlers."""
        self.running = False

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum: int, frame) -> None:
        """
        Handle shutdown signals gracefully.

        Args:
            signum: The signal number received.
            frame: The current stack frame (unused but required by API).

        """
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False

    def start(self) -> None:
        """Start the water reminder application."""
        try:
            self._validate_configuration()
            notifier = self._initialize_notifier()
            if not notifier:
                return

            scheduler = self._initialize_scheduler(notifier)
            self._run_main_loop(scheduler)

        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            logger.error("Please check your .env file and try again")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
        finally:
            logger.info("Water Reminder Bot has stopped")

    def _validate_configuration(self) -> None:
        """Validate that all required configuration is present."""
        logger.info("Loading configuration...")
        Config.validate()

    def _initialize_notifier(self) -> TelegramNotifier | None:
        """
        Initialize and test the Telegram notifier.

        Returns:
            TelegramNotifier instance if connection test succeeds,
            None otherwise.

        """
        logger.info("Initializing Telegram notifier...")
        notifier = TelegramNotifier(
            Config.TELEGRAM_BOT_TOKEN,
            Config.TELEGRAM_CHAT_ID
        )

        logger.info("Testing Telegram connection...")
        if notifier.test_connection():
            logger.info("Telegram connection test successful!")
            return notifier

        logger.error("Failed to send test message to Telegram")
        logger.error("Please check your bot token and chat ID")
        return None

    def _initialize_scheduler(self, notifier: TelegramNotifier) -> WaterReminderScheduler:
        """
        Initialize the reminder scheduler.

        Args:
            notifier: Configured Telegram notifier instance.

        Returns:
            Configured WaterReminderScheduler instance.

        """
        logger.info("Setting up reminder schedule...")
        scheduler = WaterReminderScheduler(notifier)
        logger.info(f"{scheduler.get_next_reminder()}")
        return scheduler

    def _run_main_loop(self, scheduler: WaterReminderScheduler) -> None:
        """
        Run the main application loop.

        Args:
            scheduler: Configured scheduler instance.

        """
        self._log_startup_message()
        self.running = True

        while self.running:
            scheduler.run_pending()
            time.sleep(MAIN_LOOP_INTERVAL)

    def _log_startup_message(self) -> None:
        """Log the application startup message."""
        separator = "=" * SEPARATOR_LENGTH
        logger.info(separator)
        logger.info("Water Reminder Bot is now running!")
        logger.info("Press Ctrl+C to stop")
        logger.info(separator)


def main() -> None:
    """Main entry point for the application."""
    app = WaterReminderApp()
    app.start()


if __name__ == "__main__":
    main()
