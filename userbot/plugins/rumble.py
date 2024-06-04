import asyncio

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait, Forbidden

from userbot import client, self_command_filter
from userbot.plugins.help import add_command_help


@client.on_message(self_command_filter("spam"))
@client.on_edited_message(self_command_filter("spam"))
async def spam(bot: Client, message: Message):
    to_spam = " ".join(message.command[1:-1])
    try:
        times = int(message.command[-1])
    except ValueError:
        return await message.edit('用法：`.help spam`')

    await message.delete()
    tasks = [
        bot.send_message(
            message.chat.id,
            to_spam,
            reply_to_message_id=message.reply_to_message_id,
            message_thread_id=message.reply_to_message.message_thread_id if message.reply_to_message else None

        ) for _ in range(times)]
    try:
        await asyncio.gather(*tasks)
    except (Forbidden, FloodWait, Exception):
        pass


@client.on_message(self_command_filter("re"))
@client.on_edited_message(self_command_filter("re"))
async def re(bot: Client, message: Message):
    tasks = [message.delete()]

    target_message = message.reply_to_message
    if not target_message:
        async for m in bot.get_chat_history(message.chat.id, max_id=message.id, limit=1):
            target_message = m
            break

    try:
        times = int(message.command[-1]) if len(message.command) > 1 else 1
    except ValueError:
        times = 1

    try:
        if message.chat.has_protected_content:
            tasks.extend(
                target_message.copy(
                    chat_id=target_message.chat.id,
                    message_thread_id=target_message.message_thread_id,
                    reply_to_message_id=target_message.reply_to_message_id
                ) for _ in range(times)
            )
            await asyncio.gather(*tasks)
        else:
            await asyncio.gather(*tasks)
            for _ in range(times):
                await target_message.forward(
                    chat_id=target_message.chat.id,
                    message_thread_id=target_message.message_thread_id
                )

    except (Forbidden, FloodWait, Exception):
        return


add_command_help(
    module_name="rumble",
    module_description="复读或批量发送消息。",
    commands=[
        ["spam"],
        ["re"]
    ],
    commands_description=[
        "消息轰炸某人/某群。当命令消息回复了某条消息的时候，所有后续发出的消息均会回复命令所回复的消息。",
        ("复读特定消息 n 次。当未指定消息（未回复特定消息），将会复读当前对话最新的消息。\n"
         "当对话禁用转发时此命令依然可用，但不会附带转发标志。")
    ],
    commands_example=[
        ["spam <要说的话> <复读次数> <可选:回复某条消息>", "spam 我好菜 10"],
        ["re <可选:次数> <可选:回复特定消息>", "re 3", "re <回复消息>"]

    ]
)
