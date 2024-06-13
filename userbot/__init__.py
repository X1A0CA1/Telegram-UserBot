import userbot.modules

from pyrogram import Client

from userbot.config import config
from userbot.helpers import *

from apscheduler.schedulers.asyncio import AsyncIOScheduler

VERSION = "0.0.8"

bot = app = client = Client(
    name=config.bot.name,
    api_id=config.bot.api_id,
    api_hash=config.bot.api_hash,
    bot_token=config.bot.bot_token,
    test_mode=config.bot.test_mode,
    ipv6=config.ipv6,
    app_version=f"UserBot {VERSION}",
    device_model="iPhone 18 Pro Max",
    system_version="iOS 20.5.1",
)

scheduler = AsyncIOScheduler(timezone=config.time_zone)

COMMAND_PREFIX = config.command_prefix
COMMAND_PREFIXES = config.command_prefixes
