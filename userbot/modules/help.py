from pyrogram import enums
from pyrogram.types import Message
from userbot import client, self_command_filter

from userbot import cmd_help, CommandHelp


@client.on_message(self_command_filter("help"))
async def module_help(_, message: Message):
    cmd = message.command

    if len(cmd) == 1:
        all_modules_info = cmd_help.get_all_modules_info()
        return await message.edit(all_modules_info)

    help_arg = " ".join(cmd[1:]).lower()
    if not help_arg:
        return

    module_info = cmd_help.get_module_info(help_arg)
    if module_info:
        return await message.edit(module_info, parse_mode=enums.ParseMode.HTML)

    command_info = cmd_help.get_command_info(help_arg)
    if command_info:
        return await message.edit(command_info, parse_mode=enums.ParseMode.HTML)

    return await message.edit("请指定一个有效的模块或命令名称。")


cmd_help.add_module_help(
    module_name="help",
    module_description="列出加载的模块与各个命令，也可以查看具体的模块和命令的用法。",
    commands=[
        CommandHelp(
            command=["help"],
            description="列出加载的模块与各个命令，也可以查看具体的模块和命令的用法。",
            example=["help <模块名>", "help <命令名>", "help"]
        )
    ]
)
