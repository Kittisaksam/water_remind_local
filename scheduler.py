"""
Scheduling logic for water drinking reminders.

Defines reminder times and manages scheduled jobs using the schedule library.
"""

import logging
from datetime import datetime
from typing import Final

import schedule

logger = logging.getLogger(__name__)


class WaterReminderScheduler:
    """Manages water drinking reminder schedule."""

    # Reminder messages for different times of day
    REMINDER_MESSAGES: Final = {
        "09:00": "Good morning! Time to drink water! 💧",
        "12:00": "Lunch time reminder! Stay hydrated! 🌊",
        "15:00": "Afternoon hydration break! 💦",
        "18:00": "Evening water reminder! 🚰",
        "21:00": "Last call for water today! Good night! 🌙",
    }

    def __init__(self, telegram_notifier: "TelegramNotifier") -> None:
        """
        Initialize the scheduler with a Telegram notifier.

        Args:
            telegram_notifier: Instance to send messages.

        """
        self.notifier = telegram_notifier
        self._setup_schedule()

    def _setup_schedule(self) -> None:
        """Set up the daily reminder schedule."""
        for time_str, message in self.REMINDER_MESSAGES.items():
            schedule.every().day.at(time_str).do(
                self._send_reminder, message, time_str
            )
            logger.info(f"Scheduled reminder at {time_str}")

    def _send_reminder(self, message: str, time_str: str) -> None:
        """
        Send a reminder message.

        Args:
            message: Reminder message text.
            time_str: Time string for logging purposes.

        """
        logger.info(f"Sending reminder scheduled for {time_str}")
        success = self.notifier.send_message(message)

        if success:
            logger.info(f"Reminder sent successfully at {time_str}")
        else:
            logger.error(f"Failed to send reminder at {time_str}")

    def run_pending(self) -> None:
        """Run any pending scheduled jobs."""
        schedule.run_pending()

    def get_next_reminder(self) -> str:
        """
        Get information about the next scheduled reminder.

        Returns:
            Description of next reminder time, or a message if none scheduled.

        """
        next_run = schedule.next_run()
        if next_run:
            return f"Next reminder at {next_run.strftime('%H:%M')}"
        return "No reminders scheduled"
