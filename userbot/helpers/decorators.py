import functools
import traceback

from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram import Client


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
                await message.edit(error_message)

    return wrapper
