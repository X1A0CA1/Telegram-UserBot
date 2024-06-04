from userbot import client, AioHttp, self_command_filter
from userbot.helpers import cmd_help


def replace_text(text):
    return text.replace('"', "").replace("\\r", "").replace("\\n", "").replace("\\", "")


@client.on_message(self_command_filter(["ud", "ubran"]))
@client.on_edited_message(self_command_filter(["ud", "ubran"]))
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


cmd_help.add_module_help(
    module_name="urbandictionary",
    module_description="查询 urbandictionary 一个单词短语的意思。",
    commands=[
        cmd_help.command_help(
            command=["ub", "ubran"],
            description="查询 urbandictionary 一个单词短语的意思。",
            example=["ud <词语>", "ud mogul"]
        )
    ]
)
