import asyncio
import userbot

from pyrogram import Client, compose


async def main():
    await compose(bots)


if __name__ == '__main__':
    asyncio.run(main())
