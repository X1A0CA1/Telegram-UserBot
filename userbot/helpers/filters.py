from typing import List, Union

from pyrogram import filters
from userbot.config import config


def self_command_filter(
        commands: Union[str, List[str]],
        prefixes: Union[str, List[str]] = config.command_prefixes,
        case_sensitive: bool = False
):
    return filters.command(
        commands=commands,
        prefixes=prefixes,
        case_sensitive=case_sensitive
    ) & filters.me & ~filters.forwarded & ~filters.via_bot
