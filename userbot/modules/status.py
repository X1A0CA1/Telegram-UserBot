import time
import random

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait, MessageIdInvalid

from pyrogram.raw.functions import Ping

from userbot import client, format_time, self_command_filter
from userbot.helpers import cmd_help


@client.on_message(self_command_filter("ping"))
@client.on_edited_message(self_command_filter("ping"))
async def ping(_: Client, message: Message):
    dc_ping_start_time = time.perf_counter()
    await client.invoke(Ping(ping_id=0))
    dc_ping_end_time = time.perf_counter()
    ping_duration = format_time(dc_ping_end_time - dc_ping_start_time)

    msg_process_start_time = time.perf_counter()
    message = await message.edit("Poi!")
    msg_process_end_time = time.perf_counter()
    msg_duration = format_time(msg_process_end_time - msg_process_start_time)

    await message.edit(f"Poi! | PING: **{ping_duration}** | MSG PROCESS: **{msg_duration}**")


@client.on_message(self_command_filter("stats"))
@client.on_edited_message(self_command_filter("stats"))
async def stats(_: Client, message: Message):
    msg = await message.edit("正在计算所有的聊天中... 这可能需要一些时间...")
    bot = private = group = created_group = supergroup = created_supergroup = channel = created_channel = unknown = 0
    current_count = 0
    all_chats = await client.get_dialogs_count()

    async for dialog in client.get_dialogs():
        current_count += 1
        match dialog.chat.type:
            case ChatType.BOT:
                bot += 1
            case ChatType.PRIVATE:
                private += 1
            case ChatType.GROUP:
                if dialog.chat.is_creator:
                    created_group += 1
                group += 1
            case ChatType.SUPERGROUP:
                if dialog.chat.is_creator:
                    created_supergroup += 1
                supergroup += 1
            case ChatType.CHANNEL:
                if dialog.chat.is_creator:
                    created_channel += 1
                channel += 1
            case _:
                unknown += 1
        await update_callback(all_chats, current_count, message)
    text = (
        f"**群组共计 {all_chats} 个** \n"
        f"其中：\n"
        f"私聊 {private} 个\n"
        f"临时群组 {group} 个，创建了 {created_group} 个\n"
        f"超级群组 {supergroup} 个，创建了 {created_supergroup} 个\n"
        f"频道 {channel} 个，创建了 {created_channel} 个\n"
        f"机器人私聊 {bot} 个"
    )
    text += f"\n未知类型的群组 {unknown} 个" if unknown > 0 else ""
    await msg.edit(text)


async def update_callback(all_chats, current_count, message):
    progress_percent = (current_count / all_chats) * 100

    if random.random() <= 0.003:
        try:
            await message.edit(f'当前进度 {progress_percent:.2f}% | {current_count}/{all_chats} ')
        except FloodWait:
            pass
        except MessageIdInvalid:
            raise RuntimeError('需要被编辑的消息被删除。')


cmd_help.add_module_help(
    module_name="status",
    module_description="一些统计、状态信息。",
    commands=[
        cmd_help.command_help(
            command=["ping"],
            description="测试与 Telegram 的延迟，会显示 Ping 延迟和处理消息的延迟。",
            example=["ping"]
        ),
        cmd_help.command_help(
            command=["stats"],
            description="统计你的账号所加入的不同类型的群组的数量。",
            example=["stats"]
        )
    ],
)
