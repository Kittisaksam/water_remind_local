"""
Configuration management for Water Drinking Reminder System.

Loads and validates environment variables required for the application.
"""

import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Environment variable names
ENV_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
ENV_CHAT_ID = "TELEGRAM_CHAT_ID"


class Config:
    """Configuration class for application settings."""

    TELEGRAM_BOT_TOKEN: str | None = os.getenv(ENV_BOT_TOKEN)
    TELEGRAM_CHAT_ID: str | None = os.getenv(ENV_CHAT_ID)

    @classmethod
    def validate(cls) -> None:
        """
        Validate that all required configuration is present.

        Raises:
            ValueError: If required configuration is missing or empty.

        """
        errors = []

        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append(f"{ENV_BOT_TOKEN} not set. Please add it to your .env file.")
        if not cls.TELEGRAM_CHAT_ID:
            errors.append(f"{ENV_CHAT_ID} not set. Please add it to your .env file.")

        if errors:
            raise ValueError("\n".join(errors))

        logger.info("Configuration validated successfully")
