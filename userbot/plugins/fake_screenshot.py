import asyncio

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ChatType

from pyrogram import raw

from userbot import client, error_handler, self_command_filter
from userbot.plugins.help import add_command_help


@client.on_message(self_command_filter(["ss", "screenshot"]))
@client.on_edited_message(self_command_filter(["ss", "screenshot"]))
@error_handler
async def screenshot(bot: Client, message: Message):
    if message.chat.type is not ChatType.PRIVATE:
        return await message.edit('此命令仅可在私聊使用。')

    await asyncio.gather(
        message.delete(),
        bot.invoke(
            raw.functions.messages.SendScreenshotNotification(
                peer=await bot.resolve_peer(message.chat.id),
                random_id=bot.rnd_id(),
                reply_to=raw.types.InputReplyToMessage(reply_to_msg_id=0)
            )
        ),
    )


add_command_help(
    module_name="fake_screenshot",
    module_description="发送一条当前聊天已经被截图的消息，用来恶搞，**仅可在私聊中使用**。",
    commands=[
        ["ss", "screenshot"],
    ],
    commands_description=[
        "发送一条当前聊天已经被截图的消息，用来恶搞，**仅可在私聊中使用**。"
    ],
    commands_example=[
        ["ss", "screenshot"],
    ]
)
