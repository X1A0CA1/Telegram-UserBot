import asyncio

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait, Forbidden

from userbot import client, self_command_filter
from userbot.modules.help import cmd_help


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
    except (Forbidden, FloodWait):
        pass


@client.on_message(self_command_filter("re"))
@client.on_edited_message(self_command_filter("re"))
async def re(bot: Client, message: Message):
    chat = message.chat
    tasks = [message.delete()]
    target_message = message.reply_to_message

    if not target_message:
        async for m in bot.get_chat_history(message.chat.id, max_id=message.id):
            target_message = m
            break

    try:
        times = int(message.command[-1]) if len(message.command) > 1 else 1
    except ValueError:
        times = 1

    has_protected_content = message.has_protected_content or chat.has_protected_content
    try:
        if has_protected_content and target_message.media_group_id:
            tasks.extend(
                [client.copy_media_group(
                    from_chat_id=target_message.chat.id,
                    message_id=target_message.id,
                    chat_id=message.chat.id,
                    message_thread_id=message.message_thread_id,
                    reply_to_message_id=target_message.reply_to_message_id
                ) for _ in range(times)]
            )
            await asyncio.gather(*tasks)

        elif has_protected_content and not target_message.media_group_id:
            tasks.extend(
                [target_message.copy(
                    chat_id=target_message.chat.id,
                    message_thread_id=target_message.message_thread_id,
                    reply_to_message_id=target_message.reply_to_message_id
                ) for _ in range(times)]
            )
            await asyncio.gather(*tasks)
        elif has_protected_content and target_message.media_group_id:
            await asyncio.gather(*tasks)
            target_messages = await bot.get_media_group(target_message.chat.id, target_message.id)
            for _ in range(times):
                await bot.forward_messages(
                    chat_id=message.chat.id,
                    from_chat_id=target_message.chat.id,
                    message_ids=[m.id for m in target_messages],
                    message_thread_id=message.message_thread_id
                )

        elif has_protected_content and not target_message.media_group_id:
            await asyncio.gather(*tasks)
            for _ in range(times):
                await target_message.forward(
                    chat_id=target_message.chat.id,
                    message_thread_id=target_message.message_thread_id
                )
        else:
            await asyncio.gather(*tasks)
            return

    except (Forbidden, FloodWait):
        return


@client.on_message(self_command_filter(["dre", "xre"]))
@client.on_edited_message(self_command_filter(["dre", "xre"]))
async def xre(bot: Client, message: Message):
    target_message = message.reply_to_message
    if not target_message:
        return await message.edit(f'{message.command[0]} 必须回复一条消息。')

    tasks = []
    delete_tasks = [message.delete()]

    try:
        times = int(message.command[-1]) if len(message.command) > 1 else 1
    except ValueError:
        times = 1

    if target_message.media_group_id:
        messages = await bot.get_media_group(target_message.chat.id, target_message.id)
        delete_tasks.append(bot.delete_messages(message.chat.id, [m.id for m in messages]))

        tasks.extend(
            [client.copy_media_group(
                from_chat_id=target_message.chat.id,
                message_id=target_message.id,
                chat_id=message.chat.id,
                message_thread_id=message.message_thread_id,
                reply_to_message_id=target_message.reply_to_message_id
            ) for _ in range(times)]
        )
        await asyncio.gather(*tasks)
    else:
        delete_tasks.append(target_message.delete())

        tasks.extend(
            [target_message.copy(
                chat_id=target_message.chat.id,
                message_thread_id=target_message.message_thread_id,
                reply_to_message_id=target_message.reply_to_message_id
            ) for _ in range(times)]
        )
        await asyncio.gather(*tasks)

    await asyncio.gather(*delete_tasks)


cmd_help.add_module_help(
    module_name="rumble",
    module_description="复读或批量发送消息。",
    commands=[
        cmd_help.command_help(
            command=["spam"],
            description="消息轰炸某人/某群。当命令消息回复了某条消息的时候，所有后续发出的消息均会回复命令所回复的消息。",
            example=["spam <要说的话> <复读次数> <可选:回复某条消息>", "spam 我好菜 10"]
        ),
        cmd_help.command_help(
            command=["re"],
            description=("复读特定消息 n 次。当未指定消息（未回复特定消息），将会复读当前对话最新的消息。\n"
                         "当对话禁用转发时此命令依然可用，但不会附带转发标志。"),
            example=["re <可选:次数> <可选:回复特定消息>", "re 3", "re <回复消息>"]
        ),
        cmd_help.command_help(
            command=["dre", "xre"],
            description="删掉我来发！复读消息后删掉回复的消息。",
            example=["xre <回复特定消息> <可选:次数> ", "re <回复消息> 2"]
        ),
    ],
)
