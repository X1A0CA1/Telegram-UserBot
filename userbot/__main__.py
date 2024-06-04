import platform

from userbot import bot, scheduler


if platform.system() != "Windows":
    import uvloop
    uvloop.install()

if __name__ == '__main__':
    scheduler.start()
    bot.run()
