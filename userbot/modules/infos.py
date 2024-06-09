from pyrogram import Client
from pyrogram.types import Message
from pyrogram.utils import get_channel_id

from userbot import client, self_command_filter, cmd_help, error_handler

ERROR_MESSAGE = "请输入原始 Chat ID。"


@client.on_message(self_command_filter("gcid"))
@client.on_edited_message(self_command_filter("gcid"))
@error_handler
async def cid(_: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit(ERROR_MESSAGE)

    raw_chat_id = " ".join(message.command[1:])
    if raw_chat_id.startswith("-100"):
        return await message.edit(ERROR_MESSAGE)

    if not raw_chat_id.isdigit():
        return await message.edit(ERROR_MESSAGE)

    raw_chat_id = int(raw_chat_id)
    await message.edit(f"将 {raw_chat_id} 转换为 `{get_channel_id(raw_chat_id)}`")


cmd_help.add_module_help(
    module_name="infos",
    module_description="一些实用命令，获取有关用户、群组、频道的信息。",
    commands=[
        cmd_help.command_help(
            command=["gcid"],
            description="转换原始 Chat ID 为 Pyrogram Chat ID",
            example=["gcid <原始 Chat ID>"]
        )
    ],
)
