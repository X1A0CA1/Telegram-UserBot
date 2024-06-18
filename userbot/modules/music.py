import re
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import ListenerTimeout
from pyrogram.enums import ParseMode

from userbot import client, cmd_help, error_handler, self_command_filter

SPOTIFY_REGEX_PATTERN = r'https?://open\.spotify\.com/track/[a-zA-Z0-9]+'
SPOTIFY_LINK_FILTER = (filters.me & filters.regex(SPOTIFY_REGEX_PATTERN)
                       & ~filters.forwarded & ~filters.via_bot)

CLOUD_MUSIC_REGEX_PATTERN = r'https?://music.163.com/song\?id=\d+'
CLOUD_MUSIC_FILTER = (filters.me & filters.regex(CLOUD_MUSIC_REGEX_PATTERN)
                      & ~filters.forwarded & ~filters.via_bot)

SPOTIFY_MUSIC_BOT_ID = [595898211, 6773656102]  # @DeezerMusicBot, @MusicsHuntersbot
CLOUD_MUSIC_BOT_ID = 1404457467  # @Music163bot


async def process_cloud_music_bot_req(bot: Client, message: Message, query: str) -> Message:
    try:
        cloud_music_bot_reply: Message = await bot.ask(
            filters=filters.audio,
            chat_id=CLOUD_MUSIC_BOT_ID,
            user_id=CLOUD_MUSIC_BOT_ID,
            text=query,
            timeout=30
        )
    except ListenerTimeout:
        return await message.edit("什么都没有找到 :(")
    finally:
        await bot.read_chat_history(chat_id=CLOUD_MUSIC_BOT_ID)

    if not cloud_music_bot_reply:
        return await message.edit("什么都没有找到 :(")

    cloud_music_url = None
    for key_button in cloud_music_bot_reply.reply_markup.inline_keyboard:
        if re.match(CLOUD_MUSIC_REGEX_PATTERN, key_button[0].url):
            cloud_music_url = key_button[0].url
            break
    cloud_music_bot_reply.reply_markup = cloud_music_bot_reply.entities = None
    cloud_music_bot_reply.caption = cloud_music_bot_reply.caption.replace("via @Music163bot", cloud_music_url)
    cloud_music_bot_reply.web_page_preview = False

    return await cloud_music_bot_reply.copy(
        chat_id=message.chat.id,
        reply_to_message_id=message.id
    )


@client.on_message(self_command_filter("music"))
@client.on_edited_message(self_command_filter("music"))
@error_handler
async def cloud_music(bot: Client, message: Message):
    if len(message.command) < 2:
        return await message.edit("请附带一个歌曲名或者网易云音乐链接。")
    args = " ".join(message.command[1:])
    if re.match(CLOUD_MUSIC_REGEX_PATTERN, args):
        return await process_cloud_music_bot_req(bot, message, args)
    else:
        await process_cloud_music_bot_req(bot, message, f"/music {args}")
        return await message.delete()


@client.on_message(CLOUD_MUSIC_FILTER)
@client.on_edited_message(CLOUD_MUSIC_FILTER)
async def cloud_music_link(bot: Client, message: Message):
    song_url = re.match(CLOUD_MUSIC_REGEX_PATTERN, message.text).group(0)
    return await process_cloud_music_bot_req(bot, message, song_url)


@client.on_message(SPOTIFY_LINK_FILTER)
@client.on_edited_message(SPOTIFY_LINK_FILTER)
async def spotify_link(bot: Client, message: Message):
    song_url = re.match(SPOTIFY_REGEX_PATTERN, message.text).group(0)

    async def get_bot_reply(bot_id: int, text: str):
        try:
            return await bot.ask(
                filters=filters.audio,
                chat_id=bot_id,
                user_id=bot_id,
                text=text,
                timeout=15
            )
        except ListenerTimeout:
            return None

    tasks = [asyncio.create_task(get_bot_reply(BOT_ID, song_url)) for BOT_ID in SPOTIFY_MUSIC_BOT_ID]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    for task in pending:
        task.cancel()

    spotify_music_bot_reply = None
    for task in done:
        if task.result():
            spotify_music_bot_reply = task.result()
            break

    if not spotify_music_bot_reply:
        return await message.edit(
            text=f"<b>T_T:</b>\n\n{message.text}",
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False
        )

    spotify_music_bot_reply.caption = spotify_music_bot_reply.entities = None
    await spotify_music_bot_reply.copy(
        chat_id=message.chat.id,
        reply_to_message_id=message.id
    )

    for chat_id in SPOTIFY_MUSIC_BOT_ID:
        await bot.read_chat_history(chat_id=chat_id)


cmd_help.add_module_help(
    module_name="music",
    module_description="发送来自网易云音乐，Spotify 的音乐。",
    commands=[
        cmd_help.command_help(
            command=["music"],
            description="发送音乐文件。支持关键词、歌曲数字 ID、网易云音乐链接作为参数。\n"
                        "此外，还支持直接在任意聊天发送 Spotify、网易云音乐的歌曲链接来获取歌曲。\n",
            example=["music <关键词>", "music <歌曲数字 ID>", "music <网易云音乐链接>", "<Spotify 或 网易云 音乐链接>"]
        ),
    ],
)
