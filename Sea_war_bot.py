import asyncio

from aiogram import Bot, Dispatcher

from handlers import other_handlers, user_handlers


BOT_TOKEN: str
with open("token.txt", "r") as token:
    BOT_TOKEN = token.read()


# Функция конфигурирования и запуска бота
async def main():
    bot: Bot = Bot(BOT_TOKEN, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Регистрируем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Запускаем polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())



'''
# Количество попыток, доступных пользователю в игре
ATTEMPTS: int = 40

# Словарь, в котором будут храниться данные пользователя
users: dict = {}


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет!\nДавай сыграем в игру "Угадай число"?\n\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд - отправьте команду /help')
    # Если пользователь только запустил бота и его нет в словаре '
    # 'users - добавляем его в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}
'''
