from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery

from keyboards.keyboard import yes_no_kb
from keyboards.keyboard_map import game_kb, rebuild_keyboard
from lexicon.lexicon_ru import LEXICON_RU
from services.sea_war import create_map, check_hit
from User_dict.user_dict import users

router: Router = Router()
ATTEMPTS: int = 40

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=yes_no_kb)
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'sea_map': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}


# Этот хэндлер будет срабатывать на команду "/stat"
@router.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(
                    f'Всего игр сыграно: '
                    f'{users[message.from_user.id]["total_games"]}\n'
                    f'Игр выиграно: {users[message.from_user.id]["wins"]}')


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)


# Этот хэндлер будет срабатывать на команду "/cancel"
@router.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть '
                             'снова - напишите об этом')
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer('А мы итак с вами не играем. '
                             'Может, сыграем разок?')


# Этот хэндлер срабатывает на согласие пользователя играть в игру
@router.message(Text(text=LEXICON_RU['yes_button']))
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['sea_map'] = create_map()
        users[message.from_user.id]['attempts'] = ATTEMPTS
    else:
        await message.answer('Пока мы играем в игру я могу '
                             'реагировать только на нажатие кнопок на игровом поле '
                             'и команды /cancel и /stat')


# Этот хэндлер срабатывает на отказ пользователя играть в игру
@router.message(Text(text=LEXICON_RU['no_button']))
async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_RU['no'])


# Этот хэндлер срабатывает на любую из игровых кнопок
@router.callback_query(Text(text=[str(i)+','+str(j) for i in range(1,9) for j in range(1,9)]))
async def process_game_button(callback: CallbackQuery):
    coords = callback.data.split(',')
    coord_y = int(coords[0]) - 1
    coord_x = int(coords[1]) - 1
    result = check_hit(users[callback.from_user.id]['sea_map'], coord_x, coord_y)
    await callback.message.edit_text(
        text=LEXICON_RU[result],
        reply_markup=rebuild_keyboard(callback.message.reply_markup.inline_keyboard, coord_x, coord_y, result))
    await callback.answer()