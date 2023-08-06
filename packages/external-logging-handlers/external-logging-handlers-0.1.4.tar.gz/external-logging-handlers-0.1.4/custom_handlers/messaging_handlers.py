import asyncio
import json
from typing import Any

import aiohttp as aiohttp
from starlette.responses import Response

from custom_handlers import (
    default_discord_webhook,
    default_telegram_channel,
    default_telegram_token,
    default_telegram_parse_mode,
    default_embeds_title,
    default_regular_message_text,
    default_sender_name,
)


class AbstractMessaging:
    """Abstract class for sending messages to different sources"""

    def __init__(
        self,
        message_delay: int = 1,
    ):
        self.message_delay = message_delay

    async def async_request(
        self, session_kwargs: dict, request_kwargs: dict
    ) -> Response:
        """Asynchronous request to endpoint

        :param session_kwargs: kwargs for aiohttp.ClientSession
        :param request_kwargs: kwargs for aiohttp.ClientSession.request
        :return: starlette Response
        """

        async with aiohttp.ClientSession(**session_kwargs) as session:
            await asyncio.sleep(self.message_delay)
            async with session.request(**request_kwargs) as response:
                if 300 > response.status >= 200:
                    return Response(
                        content=json.dumps(await response.text()), status_code=200
                    )
                return Response(
                    content=json.dumps(await response.text()),
                    status_code=response.status,
                )

    async def send_message(
        self,
        session_kwargs: dict,
        request_kwargs: dict,
        text: str,
    ) -> Response:
        """Method for sending messages to a webhook"""
        request_kwargs.update({"data": text})
        await asyncio.sleep(self.message_delay)
        return await self.async_request(
            session_kwargs=session_kwargs,
            request_kwargs=request_kwargs,
        )


class DiscordMessaging(AbstractMessaging):
    """Class for messaging with Discord bot hook"""

    def __init__(
        self,
        sender_name: str = default_sender_name,
        regular_message_text: str = default_regular_message_text,
        embeds_title: str = default_embeds_title,
        webhook_url: str = default_discord_webhook,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.webhook_url = webhook_url
        self.sender_name = sender_name
        self.regular_message_text = regular_message_text
        self.embeds_title = embeds_title

    async def send_message(
        self,
        session_kwargs: dict,
        request_kwargs: dict,
        text: str,
    ) -> Response:
        """Sending message to discord using bot webhook
        Message that was sent to discord must have special formatting
        """
        data = {
            "url": self.webhook_url,
            "json": {
                "username": self.sender_name,
                "content": self.regular_message_text,
                "embeds": [{"title": self.embeds_title, "description": text}],
            },
        }
        request_kwargs.update(data)
        return await self.async_request(
            session_kwargs=session_kwargs,
            request_kwargs=request_kwargs,
        )


class TelegramMessaging(AbstractMessaging):
    """Interactions with telegram
    (sending message to channel / user only)"""

    def __init__(
        self,
        channel_id: str = default_telegram_channel,
        token: str = default_telegram_token,
        parse_mode: str = default_telegram_parse_mode,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.channel_id = channel_id
        self.token = token
        self.root = f"https://api.telegram.org/bot{self.token}/" + "{method}"
        self.update_polls_command = self.root.format(method="getUpdates")
        self.parse_mode = parse_mode
        self.send_message_method = (
            "sendMessage?chat_id={chat_id}&parse_mode={parse_mode}"
        )
        self.send_message_command = self.root.format(method=self.send_message_method)

    async def send_message(
        self, session_kwargs: dict, request_kwargs: dict, text: str
    ) -> Response:
        """Async sending message"""
        url = self.send_message_command.format(
            chat_id=self.channel_id, parse_mode=self.parse_mode
        )
        json_data = {"text": text}
        request_kwargs.update({"url": url, "json": json_data})
        return await self.async_request(
            session_kwargs=session_kwargs, request_kwargs=request_kwargs
        )
