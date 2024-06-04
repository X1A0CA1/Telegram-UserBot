from typing import List, Dict, Optional
from userbot.config import config


class CommandConflictError(Exception):
    def __init__(self, command: List):
        super().__init__(f"命令冲突: 尝试导入命令 {command} 时出现冲突。")
        self.command = command

    def __str__(self):
        return f"命令冲突: 尝试导入命令 {self.command} 时出现冲突。"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.command})"


class CommandHelp:
    def __init__(self, command: List[str], description: str, example: Optional[List[str]] = None):
        self.command = command
        self.description = description
        self.example = example

    def format_command(self):
        command_list = example_list = ""

        if self.command:
            command_list = " | ".join([f"<code>{config.command_prefix}{cmd}</code>" for cmd in self.command])
        if self.example:
            example_list += "例："
            example_list += " | ".join([f"<code>{config.command_prefix}{exp}</code>" for exp in self.example])
        return f"-> {command_list}\n{self.description}\n{example_list}\n\n"


class ModuleHelp:
    def __init__(self, module_name: str, module_description: str):
        self.module_name = module_name
        self.module_description = module_description
        self.commands: List[CommandHelp] = []

    def add_command(self, command_help: CommandHelp):
        self.commands.append(command_help)

    def format_module(self):
        heading = f"──「 <b>{self.module_name.upper()}</b> 」──\n\n"
        module_info = f"<b>模块描述:</b>\n{self.module_description}\n\n"
        command_info = "".join([cmd.format_command() for cmd in self.commands])
        return f"<b>Help for</b>\n{heading}{module_info}{command_info}"


class CMDHelp:
    def __init__(self):
        self.modules: Dict[str, ModuleHelp] = {}

    def add_module_help(self, module_name: str, module_description: str, commands: Optional[List[CommandHelp]]):
        if module_name not in self.modules:
            self.modules[module_name] = ModuleHelp(module_name, module_description)
        module = self.modules[module_name]
        for command in commands:
            self.check_exist(command)
            module.add_command(command)

    def get_all_modules_info(self):
        all_commands = "<b>已加载的模块:</b>\n\n<blockquote>"
        num_modules = len(self.modules)
        for index, module in enumerate(sorted(self.modules.values(), key=lambda m: m.module_name)):
            command_list = " | ".join([f"<code>{cmd}<code>" for command in module.commands for cmd in command.command])
            if not command_list:
                command_list = "<b>此模块没有命令。</b>"
            all_commands += f"<b>{module.module_name}</b>: {module.module_description}\n命令: {command_list}"
            # 判断是否为最后一个模块，不是的话添加换行
            if index < num_modules - 1:
                all_commands += "\n\n"
        all_commands += f"</blockquote>\n\n<b>使用 <code>{config.command_prefix}help <模块名|命令名></code> 来查看模块的详细信息。</b>\n"
        all_commands += f"<b>当前命令前缀:</b> <code><b>{' '.join(config.command_prefixes)}</b></code>"
        return all_commands

    def get_module_info(self, module_name: str):
        if module_name in self.modules:
            return self.modules[module_name].format_module()
        return None

    def get_command_info(self, command_name: str):
        for module in self.modules.values():
            for cmd in module.commands:
                if command_name in cmd.command:
                    return module.format_module()
        return None

    def check_exist(self, command: CommandHelp):
        for module in self.modules.values():
            for cmd in module.commands:
                if set(command.command) & set(cmd.command):
                    raise CommandConflictError(command.command)

    @staticmethod
    def command_help(*args, **kwargs):
        return CommandHelp(*args, **kwargs)


cmd_help = CMDHelp()
