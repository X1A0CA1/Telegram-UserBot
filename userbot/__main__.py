import uvloop

from userbot import bot, scheduler

uvloop.install()

if __name__ == '__main__':
    scheduler.start()
    bot.run()
