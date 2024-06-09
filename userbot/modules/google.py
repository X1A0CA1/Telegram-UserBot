import io
import os
import time
import re

from asyncio import sleep

from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from search_engine_parser import GoogleSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError

from pyrogram.types import Message
from pyrogram.enums import ParseMode

from userbot import client, self_command_filter, cmd_help, error_handler

options = Options()
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-gpu")
options.add_argument("--headless=new")
options.add_argument("--test-type")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920x1080")
options.add_experimental_option(
    "prefs", {
        "download.default_directory": f"{os.getcwd()}/temp"
    },
)


def is_valid_url(text: str) -> bool:
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


@client.on_message(self_command_filter("webshot"))
@client.on_edited_message(self_command_filter("webshot"))
@error_handler
async def web_screenshot(_, message: Message):
    if len(message.command) < 2:
        return await message.edit("请附带一个 URL。")

    url = " ".join(message.command[1:])
    if not re.match(r'https?://', url):
        url = 'https://' + url
    if not is_valid_url(url):
        return await message.edit("无效的 URL。")

    await message.edit(f"启动浏览器中...")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    image = None
    try:
        await message.edit("访问并截图中...")
        driver.get(url)
        await sleep(1)
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
            "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )

        driver.set_window_size(1920, height)
        await sleep(1)
        image = driver.get_screenshot_as_png()
    except Exception as e:
        driver.close()
        driver.quit()
        return await message.edit("截图失败，可能是你的网址无法访问，错误信息：\n\n" + str(e))

    driver.close()
    driver.quit()

    if not image:
        return await message.edit("截图失败，未知错误。")

    with io.BytesIO(image) as result:
        result.name = f"{url}_{time.time()}.png"
        await message.reply_document(result)
        await message.delete()


@client.on_message(self_command_filter("google"))
@client.on_edited_message(self_command_filter("google"))
@error_handler
async def google_search(_, message: Message):
    if len(message.command) < 2:
        return await message.edit("请输入搜索词。")

    search_query = " ".join(message.command[1:])

    await message.edit(f"Google 搜索中...")

    try:
        search = GoogleSearch()
        results = await search.async_search(query=search_query, page=1, safe="off", cache=False)
    except NoResultsOrTrafficError:
        return await message.edit(
            f"<b>搜索 <code>{search_query}</code> 返回了空结果。</b>\n"
            f"这可能是你的IP被 Google 限制了，亦或者可能是这个关键词被 Google 限制了。总之就是什么都没找到。"
        )
    except Exception as error:
        return await message.edit(f"搜索 <code>{search_query}</code> 时出现错误：\n\n{error}")

    text = f"🔍 搜索了 <code>{search_query}</code>，找到了这些玩意儿:</b> \n\n<blockquote expandable>"
    for result in results:
        text += f"🌐: <a href=\"{result['links']}\">{result['titles']}</a>\n"
        text += f"📖: {result['descriptions'][:100]}...\n\n"
    text += "</blockquote>"

    await message.edit(text, disable_web_page_preview=True, parse_mode=ParseMode.HTML)


cmd_help.add_module_help(
    module_name="google",
    module_description="Google 搜索、网页截图等。",
    commands=[
        cmd_help.command_help(
            command=["google"],
            description="在 Google 上搜索某个东西",
            example=["google <关键词>"]
        ),
        cmd_help.command_help(
            command=["webshot"],
            description="进行网页截图",
            example=["webshot <网页链接>"]
        )
    ],
)
