import platform
import asyncio

from userbot import bot, scheduler, load_modules_and_plugins
from pyrogram import idle

if platform.system() != "Windows":
    import uvloop

    uvloop.install()


async def main():
    scheduler.start()
    await bot.start()
    await load_modules_and_plugins()
    await idle()


if __name__ == '__main__':
    asyncio.run(main())
