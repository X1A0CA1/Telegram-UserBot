from pyrogram import Client

from userbot.config import config

VERSION = "0.0.1"


bot = app = client = Client(
    name=config.bot.name,
    api_id=config.bot.api_id,
    api_hash=config.bot.api_hash,
    bot_token=config.bot.bot_token,
    test_mode=config.bot.test_mode,
    plugins=dict(root="userbot/plugins", external="plugins"),
    ipv6=config.ipv6,
    app_version=f"UserBot {VERSION}",
    device_model="iPhone 18 Pro Max",
    system_version="iOS 20.5.1",
)

