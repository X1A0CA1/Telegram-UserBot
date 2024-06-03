from pyrogram import filters

from userbot import client, AioHttp
from userbot.plugins.help import add_command_help


def replace_text(text):
    return text.replace('"', "").replace("\\r", "").replace("\\n", "").replace("\\", "")


@client.on_message(filters.me & filters.command(["ud"], "."))
@client.on_edited_message(filters.me & filters.command(["ud"], "."))
async def urban_dictionary(_, message):
    if len(message.text.split()) == 1:
        return await message.edit("用法: `ud <需要查询的词语>`")

    try:
        text = message.text.split(None, 1)[1]
        response = await AioHttp().get_json(
            f"https://api.urbandictionary.com/v0/define?term={text}"
        )
        word = response["list"][0]["word"]
        definition = response["list"][0]["definition"]
        example = response["list"][0]["example"]
        resp = (
            f"**Text: {replace_text(word)}**\n"
            f"**Meaning:**\n`{replace_text(definition)}`\n\n"
            f"**Example:**\n`{replace_text(example)}` "
        )
        await message.edit(resp)
        return
    except Exception as e:
        return await message.edit(
            f"UD 的 API 好像爆炸了，这里是错误信息:\n"
            f"<blockquote expandable>{e}<pre></pre></blockquote>"
        )

add_command_help(
    module_name="urbandictionary",
    module_description="查询 urbandictionary 词语意思。",
    commands=[
        [".ubran", ".ud"],
    ],
    commands_description=[
        "查询 urbandictionary 一个词是什么意思。",
    ],
    commands_example=[
        [".ud <词语>", ".ud mogul"],
    ]
)
