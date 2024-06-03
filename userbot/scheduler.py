from apscheduler.schedulers.asyncio import AsyncIOScheduler

from userbot.config import config

scheduler = AsyncIOScheduler(timezone=config.TIME_ZONE)
