from typing import List

from pyrogram import filters, enums
from pyrogram.types import Message
from userbot import client, CMD_HELP

heading = "──「 **{0}** 」──\n\n"


def split_list(input_list, n):
    n = max(1, n)
    return [input_list[i: i + n] for i in range(0, len(input_list), n)]


@client.on_message(filters.command("help", ".") & filters.me)
async def module_help(_, message: Message):
    cmd = message.command

    if len(cmd) == 1:
        all_commands = "**已加载的插件：**\n\n"

        for module in sorted(CMD_HELP.keys()):
            commands = CMD_HELP[module]['commands']
            command_list = " | ".join(
                [f"`{cmd}`" for sublist in [cmd_info['command'] for cmd_info in commands] for cmd in sublist])
            all_commands += f"**{module}**: {CMD_HELP[module]['module_description']}\n命令: {command_list}\n\n"

        return await message.edit(all_commands)

    help_arg = " ".join(cmd[1:])
    if not help_arg:
        return
    help_arg = help_arg.lower()
    if help_arg in CMD_HELP:
        commands: dict = CMD_HELP[help_arg]
        this_command = "**Help for**\n"
        this_command += heading.format(str(help_arg)).upper()

        this_command += f"**模块描述:**\n{commands['module_description']}\n\n"

        for cmd_info in commands['commands']:
            this_command += f"-> {' | '.join([f'`{cmd}`' for cmd in cmd_info['command']])}\n"
            this_command += f"{cmd_info['description']}\n"
            this_command += f"例：{' | '.join([f'`{exp}`' for exp in cmd_info['example']])}\n\n"

        return await message.edit(this_command, parse_mode=enums.ParseMode.MARKDOWN)

    # 如果查询的不是模块，则在子命令里寻找 help_arg
    found = False
    if not help_arg.startswith('.'):
        help_arg = f".{help_arg}"
    for module in CMD_HELP:
        for cmd_info in CMD_HELP[module]['commands']:
            if help_arg in cmd_info['command']:
                this_command = "**Help for**\n"
                this_command += heading.format(str(module)).upper()

                this_command += f"**模块描述:**\n{CMD_HELP[module]['module_description']}\n\n"

                this_command += f"-> {' | '.join([f'`{cmd}`' for cmd in cmd_info['command']])}\n"
                this_command += f"{cmd_info['description']}\n"
                this_command += f"例：{' | '.join([f'`{exp}`' for exp in cmd_info['example']])}\n\n"
                await message.edit(this_command, parse_mode=enums.ParseMode.MARKDOWN)
                found = True
                break
        if found:
            break

    if not found:
        return await message.edit(
            "`请指定一个有效的模块或命令名称。`", parse_mode=enums.ParseMode.MARKDOWN
        )


def add_command_help(
        module_name: str,
        module_description: str,
        commands: List[list],
        commands_description: List[str],
        commands_example: List[list]
):
    if module_name in CMD_HELP.keys():
        command_dict = CMD_HELP[module_name]
    else:
        command_dict = {}

    command_dict['commands'] = []

    for cmds, cmd_des, cmd_exp in zip(commands, commands_description, commands_example):
        command_dict['commands'].append({
            'command': cmds,
            'description': cmd_des,
            'example': cmd_exp
        })

    command_dict['module_description'] = module_description
    CMD_HELP[module_name] = command_dict


add_command_help(
    module_name="help",
    module_description="列出加载的模块与各个命令，你可以使用 `.help help` 来查看 help 的用法。",
    commands=[
        [".help"],
    ],
    commands_description=[
        "列出加载的模块与各个命令的用法。",
    ],
    commands_example=[
        [".help <模块名>", ".help <命令名>", ".help"],
    ]
)
