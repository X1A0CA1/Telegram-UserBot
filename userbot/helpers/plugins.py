import userbot
import importlib


async def load_modules_and_plugins():
    for module_name in userbot.modules.module_list.copy():
        try:
            importlib.import_module(f"userbot.modules.{module_name}")
            print(f"已加载 {module_name}")
        except BaseException as exception:
            print(f"导入内部模块 {module_name} 出现错误: {type(exception)}: {exception}")

    for plugin_name in userbot.modules.plugin_list.copy():
        try:
            importlib.import_module(f"plugins.{plugin_name}")
            print(f"已加载 {plugin_name}")
        except BaseException as exception:
            print(f"导入插件 {plugin_name} 出现错误: {type(exception)}: {exception}")
            userbot.modules.plugin_list.remove(plugin_name)
