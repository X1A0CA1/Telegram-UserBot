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

from pyrogram.types import Message

from userbot import client, self_command_filter, cmd_help

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
        # width = driver.execute_script(
        #     "return Math.max(document.body.scrollWidth, document.body.offsetWidth, "
        #     "document.documentElement.clientWidth,"
        #     "document.documentElement.scrollWidth, document.documentElement.offsetWidth);"
        # )

        driver.set_window_size(1920, height)
        # await sleep(1)
        image = driver.get_screenshot_as_png()
    except Exception:
        pass
    finally:
        driver.close()
        driver.quit()

    if not image:
        return await message.edit("截图失败。")

    with io.BytesIO(image) as result:
        result.name = f"{url}_{time.time()}.png"
        await message.reply_document(result)
        await message.delete()
