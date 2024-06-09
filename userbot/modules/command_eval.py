import asyncio
import io
import os
import sys
import traceback
import platform
import time

from pyrogram import Client
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import Message

from userbot import client, format_time, error_handler, self_command_filter
from userbot.modules.help import cmd_help


@client.on_message(self_command_filter("eval"))
@client.on_edited_message(self_command_filter("eval"))
@error_handler
async def eval_func_edited(bot, message):
    await evaluation_func(bot, message)


async def evaluation_func(bot: Client, message: Message):
    cmd = message.text.split(" ", maxsplit=1)[1]
    await message.edit(f"<pre language=python>{cmd}</pre>", parse_mode=ParseMode.HTML)

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    start_time = time.perf_counter()
    try:
        await await_exec(cmd, bot, message)
    except Exception as e:
        exc = f"{e}\n{traceback.format_exc()}"

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "执行成功"

    final_output = (f"<b>执行耗时 {format_time(execution_time)}</b>:\n"
                    f"<blockquote expandable><pre>{evaluation.strip()}</pre></blockquote>")
    if len(final_output) > 4096:
        with open("eval.txt", "w", encoding="utf8") as out_file:
            out_file.write(str(final_output))

        await message.reply_document(
            "eval.txt",
            disable_notification=True,
            reply_to_message_id=message.id,
            parse_mode=ParseMode.HTML
        )
        os.remove("eval.txt")
    else:
        await message.reply(final_output, parse_mode=ParseMode.HTML)


async def await_exec(code, bot, message):
    exec(
        f"async def __await_exec(bot, message):\n"
        f"    msg = message\n"
        f"    me = bot.me\n"
        f"    chat = message.chat\n"
        f"    reply = message.reply_to_message if message else None\n"
        f"    client = app = bot\n"
        + "".join(f"    {line}\n" for line in code.split("\n"))
    )
    return await locals()["__await_exec"](bot, message)


@client.on_edited_message(self_command_filter("sh"))
@client.on_message(self_command_filter("sh"))
@error_handler
async def execution_func_edited(bot, message):
    await execution(bot, message)


async def execution(_: Client, message: Message):
    cmd = message.text.split(" ", maxsplit=1)[1]
    await message.edit(f"<pre language=shell>{cmd}</pre>")

    start_time = time.perf_counter()
    if platform.system() == 'Windows':
        encoding = 'gbk'
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, shell=True
        )
    else:
        encoding = 'utf-8'
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    stdout, stderr = await process.communicate()

    o = stdout.decode(encoding, errors="replace")
    e = stderr.decode(encoding, errors="replace")

    output = ""
    output += (f"<b>执行耗时 {format_time(execution_time)}</b>: \n"
               f"<blockquote expandable><pre>{o if o else '无输出'}</pre></blockquote>\n")
    output += f"<b>错误</b>: \n<blockquote expandable><pre>{e}</pre></blockquote>" if e else ""

    if len(output) > 4096:
        with open("sh.txt", "w+", encoding="utf8") as out_file:
            out_file.write(str(output))

        await message.reply_document(
            document="sh.txt",
            disable_notification=True,
            reply_to_message_id=message.id,
        )
        os.remove("sh.txt")
    else:
        await message.reply(output)


cmd_help.add_module_help(
    module_name="command_eval",
    module_description="执行 python3 或 系统命令，注意，请不要随意执行陌生人的命令，<b>这可能会导致你的账号被盗或其他风险</b>。",
    commands=[
        cmd_help.command_help(
            command=["eval"],
            description="执行 python3 命令。",
            example=["eval print('Hello World')"]
        ),
        cmd_help.command_help(
            command=["sh"],
            description="执行系统命令。",
            example=["sh ls"]
        )
    ],
)
