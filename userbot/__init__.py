from pyrogram import Client

from userbot.config import config
from userbot.helpers import *

from apscheduler.schedulers.asyncio import AsyncIOScheduler

VERSION = "0.0.3"


bot = app = client = Client(
    name=config.bot.name,
    api_id=config.bot.api_id,
    api_hash=config.bot.api_hash,
    bot_token=config.bot.bot_token,
    test_mode=config.bot.test_mode,
    plugins=dict(root=f"userbot/plugins"),
    ipv6=config.ipv6,
    app_version=f"UserBot {VERSION}",
    device_model="iPhone 18 Pro Max",
    system_version="iOS 20.5.1",
)

scheduler = AsyncIOScheduler(timezone=config.time_zone)


# 一些变量们
CMD_HELP = {}

COMMAND_PREFIX = config.command_prefixes[0] if type(config.command_prefixes) is list else config.command_prefixes
