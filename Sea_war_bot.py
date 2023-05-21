import asyncio

from aiogram import Bot, Dispatcher

from handlers import other_handlers, user_handlers, one_sided_handlers, pair_AI_handlers, pair_human_handlers


BOT_TOKEN: str
with open("token.txt", "r") as token:
    BOT_TOKEN = token.read()


# Функция конфигурирования и запуска бота
async def main():
    bot: Bot = Bot(BOT_TOKEN, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Регистрируем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(one_sided_handlers.router)
    dp.include_router(pair_AI_handlers.router)
    dp.include_router(pair_human_handlers.router)
    dp.include_router(other_handlers.router)

    # Запускаем polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
