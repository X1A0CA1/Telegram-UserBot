import os
from glob import glob


def list_files_in_directory(directory, pattern="*.py", exclude_init=True):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_paths = glob(os.path.join(directory, pattern))
    return [
        os.path.basename(file)[:-3]
        for file in file_paths
        if os.path.isfile(file) and (not exclude_init or not file.endswith("__init__.py"))
    ]


def format_list_as_string(items):
    return ", ".join(items)


module_list = sorted(list_files_in_directory(os.path.dirname(__file__)))
plugin_list = sorted(list_files_in_directory(os.path.join(os.getcwd(), "plugins")))

module_list_string = format_list_as_string(module_list)
plugin_list_string = format_list_as_string(plugin_list)


__all__ = module_list + ["module_list"] + plugin_list + ["plugin_list"]
