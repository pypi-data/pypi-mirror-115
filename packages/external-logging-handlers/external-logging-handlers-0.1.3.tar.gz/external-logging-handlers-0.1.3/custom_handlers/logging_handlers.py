"""Discord and Telegram Handlers async
 Handlers for logging"""

import asyncio
from logging import Formatter, StreamHandler

from custom_handlers import (
    default_formatter,
    default_telegram_parse_mode,
    default_telegram_token,
    default_telegram_channel,
    default_discord_webhook,
    default_embeds_title,
    default_regular_message_text,
    default_sender_name,
)
from custom_handlers.messaging_handlers import DiscordMessaging, TelegramMessaging


class DiscordHandler(StreamHandler):
    """Telegram handler for logging
    that supports async sending data to
    telegram via telegram bot"""

    method = "POST"

    def __init__(
        self,
        formatter: Formatter = default_formatter,
        sender_name: str = default_sender_name,
        regular_message_text: str = default_regular_message_text,
        embeds_title: str = default_embeds_title,
        webhook_url: str = default_discord_webhook,
        *args,
        **kwargs
    ):
        """
        Setup DiscordHandler class
        """
        super().__init__(*args, **kwargs)
        self.bot = DiscordMessaging(
            sender_name,
            regular_message_text,
            embeds_title,
            webhook_url,
        )
        self.formatter: formatter = formatter

    def emit(self, record):
        """Logging handler built-in method, that was overridden
        to send messages"""
        request_kwargs = {"method": DiscordHandler.method}
        session_kwargs = {}
        if self.formatter:
            msg = self.formatter.format(record) + self.terminator
        else:
            msg = record.msg + self.terminator
        if len(msg) >= 400:
            msg = msg[:200:] + "|end|" + msg[len(msg) - 200 : :]
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(
                self.bot.send_message(
                    request_kwargs=request_kwargs,
                    session_kwargs=session_kwargs,
                    text=msg,
                )
            )
        except RuntimeError:
            asyncio.run(
                self.bot.send_message(
                    request_kwargs=request_kwargs,
                    session_kwargs=session_kwargs,
                    text=msg,
                )
            )


class TelegramHandler(StreamHandler):
    """Special telegram handler for logging
    that supports sync and async sending data to
    telegram via telegram bot"""

    method = "POST"

    def __init__(
        self,
        formatter: Formatter = default_formatter,
        channel_id: str = default_telegram_channel,
        token: str = default_telegram_token,
        parse_mode: str = default_telegram_parse_mode,
        *args,
        **kwargs
    ):
        """
        Setup TelegramHandler class
        """
        super().__init__(*args, **kwargs)
        self.bot = TelegramMessaging(channel_id, token, parse_mode, *args, **kwargs)
        self.formatter: Formatter = formatter

    def emit(self, record):
        """Logging handler built-in method, that was overridden
        to send messages"""
        request_kwargs = {"method": TelegramHandler.method}
        session_kwargs = dict()

        if self.formatter:
            msg = self.formatter.format(record) + self.terminator
        else:
            msg = record.msg + self.terminator

        if len(msg) >= 400:
            msg = msg[:200:] + "|end|" + msg[len(msg) - 200 : :]
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(
                self.bot.send_message(
                    request_kwargs=request_kwargs,
                    session_kwargs=session_kwargs,
                    text=msg,
                )
            )
        except RuntimeError:
            asyncio.run(
                self.bot.send_message(
                    request_kwargs=request_kwargs,
                    session_kwargs=session_kwargs,
                    text=msg,
                )
            )
