import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from config import BOT_TOKEN
from handlers.command_handlers import command_router
from handlers.message_handlers import message_router


async def main():
    bot = Bot(
        token = BOT_TOKEN,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )
    await bot.set_my_commands(
        commands=[
            BotCommand(command='start', description='Start/restart bot'),
            BotCommand(command='help', description='Manual for using bot'),
            BotCommand(command='courses', description='Currency courses'),
            BotCommand(command='week', description='Currency courses in the week'),
            BotCommand(command='usd', description='USD course'),
            BotCommand(command='eur', description='EURO course'),
            BotCommand(command='ruble', description='Russian ruble course'),
        ]
    )
    dp = Dispatcher()
    dp.include_routers(command_router,message_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
