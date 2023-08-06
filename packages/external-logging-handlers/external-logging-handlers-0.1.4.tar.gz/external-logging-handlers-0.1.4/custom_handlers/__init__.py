import os
from logging import Formatter

default_formatter = Formatter(
    f'{os.environ.get("SERVER_NAME")} - %(asctime)s - '
    f"%(name)s - %(levelname)s - %(message)s"
)

default_telegram_channel = os.environ.get("TELEGRAM_CHANNEL_ID")
default_telegram_token = os.environ.get("TELEGRAM_TOKEN")
default_telegram_parse_mode = "HTML"

default_server_name = os.environ.get("SERVER_NAME")
default_discord_webhook = os.environ.get("DISCORD_WEBHOOK_URL")

default_sender_name = os.environ.get("SENDER_NAME")
default_regular_message_text = os.environ.get("REGULAR_MESSAGE_TEXT")
default_embeds_title = os.environ.get("EMBEDS_TITLE")
