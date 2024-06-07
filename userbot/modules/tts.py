import io
import time
import emoji

import azure.cognitiveservices.speech as speech_sdk

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import VoiceMessagesForbidden
from pyrogram.enums import ChatType

from pyrogram.raw.functions.users import GetFullUser

from userbot import client, self_command_filter, cmd_help, config


speech_key = config.plugins.azure_speech_key
service_region = config.plugins.azure_service_region

if not speech_key or not service_region:
    raise ValueError("未填写 azure 相关配置项，tts 将被禁用。")


@client.on_message(self_command_filter(["tts"]))
async def text_to_voice(bot: Client, message: Message):
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    else:
        return await message.edit("回复一条消息或者输入文本来转换为语音，输入文本的优先级大于回复消息。")
    if not text:
        return await message.edit("没有检测到文本？")

    # 判断当前聊天是否能发送语音。
    if message.chat.type is ChatType.PRIVATE:
        # 获取 full user
        full_user = await bot.invoke(
            GetFullUser(
                id=await client.resolve_peer(message.chat.id)
            )
        )
        if full_user.full_user.voice_messages_forbidden:
            return await message.edit("当前聊天不允许发送语音 T_T")
    elif message.chat.type is ChatType.SUPERGROUP:
        if message.chat.permissions \
                and not (message.chat.permissions.can_send_media_messages or message.chat.permissions.can_send_voices):
            return await message.edit("当前聊天不允许发送语音 T_T")

    # 删掉所有的 emoji
    text = emoji.replace_emoji(text, "")

    await message.edit("等待 M$ 响应中...")

    speech_config = speech_sdk.SpeechConfig(
        subscription=speech_key,
        region=service_region
    )
    speech_config.speech_recognition_language = 'zh-CN'
    speech_config.speech_synthesis_voice_name = 'zh-CN-XiaoxiaoMultilingualNeural'

    speech_config.set_speech_synthesis_output_format(speech_sdk.SpeechSynthesisOutputFormat.Ogg24Khz16BitMonoOpus)

    speech_synthesizer = speech_sdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=None
    )
    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        pass
    elif result.reason == speech_sdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        if cancellation_details.reason == speech_sdk.CancellationReason.Error:
            return await message.edit(f"语音转换出现错误，错误详情：{cancellation_details.error_details}。")

    if not result.audio_data:
        return await message.edit("语音转换失败。")

    with io.BytesIO(result.audio_data) as opus_bytes_io:
        opus_bytes_io.name = f"AZURE_TTS_{time.time()}.ogg"
        try:
            await bot.send_voice(
                message.chat.id,
                opus_bytes_io,
                reply_to_message_id=message.reply_to_message_id,
                message_thread_id=message.message_thread_id
            )
        except VoiceMessagesForbidden:
            return await message.edit("当前聊天不允许发送语音 T_T")
        await message.delete()


cmd_help.add_module_help(
    module_name="tts",
    module_description="将一段话转为语音。",
    commands=[
        cmd_help.command_help(
            command=["tts"],
            description="可以回复一条带有文本的消息，将其转为语音，或者带入文本参数，文本参数的优先级始终大于回复消息。",
            example=["tts <回复某条消息>", "tts <要说的话>", "tts The quick brown fox jumped over the lazy dog."]
        ),
    ],
)
