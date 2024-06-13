import functools
import traceback
import time
import cProfile
import pstats
from io import StringIO

from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram import Client

from .utils import format_time


def error_handler(func):
    @functools.wraps(func)
    async def wrapper(client: Client, message: Message, *args, **kwargs):
        try:
            await func(client, message, *args, **kwargs)
        except Exception as e:
            error_message = (
                f"<b>执行命令发生错误</b>: \n\n"
                f"<blockquote expandable><pre>"
                f"{''.join(traceback.format_exception(None, e, e.__traceback__))}"
                f"</pre></blockquote expandable>"
            )

            if len(error_message) >= 4000:
                with open("eval.txt", "w", encoding="utf8") as out_file:
                    out_file.write(error_message)

                await message.reply_document(
                    document="error.txt",
                    caption=f"<b>执行命令出现错误</b>",
                    disable_notification=True,
                    reply_to_message_id=message.id,
                    parse_mode=ParseMode.HTML
                )
            else:
                await message.edit(error_message, parse_mode=ParseMode.HTML)

    return wrapper


def send_command_process_time(func):
    @functools.wraps(func)
    async def wrapper(client: Client, message: Message, *args, **kwargs):
        start_time = time.perf_counter()
        result = await func(client, message, *args, **kwargs)
        end_time = time.perf_counter()
        p_time = end_time - start_time

        speedtest_message = (
            f"<b>命令处理耗时</b>: {format_time(p_time)} "
        )

        await client.send_message(
            chat_id=message.chat.id,
            text=speedtest_message,
            disable_notification=True,
            reply_to_message_id=message.id,
            parse_mode=ParseMode.HTML
        )

        return result

    return wrapper


def cprofile_async(func):
    async def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = await func(*args, **kwargs)
        pr.disable()

        s = StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('time')
        ps.print_stats()

        print(s.getvalue())

        return result

    return wrapper
