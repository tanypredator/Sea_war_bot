from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery

from keyboards.keyboard import yes_no_kb, game_mode_kb
from keyboards.keyboard_map import game_kb, rebuild_keyboard
from keyboards.pair_AI_keyboard import pair_AI_game_kb
from lexicon.lexicon_ru import LEXICON_RU
from services.sea_war import create_map, shot_result, player_map
from User_dict.user_dict import users

router: Router = Router()
ATTEMPTS: int = 40
TILES_LEFT = 13
SHIPS_LEFT: int = 7

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=game_mode_kb)
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
        'game_mode': None,
                                       'AI_map': None,
                                       'player_map': None,
                                       'attempts': None,
                                       'ships_left': None,
                                       'hits': None,
                                       'tiles_left': None,
                                       'tiles': None,
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
    await message.answer(text=LEXICON_RU['/help'], reply_markup=game_mode_kb)


# Этот хэндлер будет срабатывать на команду "/cancel"
@router.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть '
                             'снова - напишите об этом')
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer(text ='А мы итак с вами не играем. '
                             'Может, сыграем разок?', reply_markup=game_mode_kb)


# Этот хэндлер срабатывает на выбор пользователя играть в игру без своего поля
@router.message(Text(text=LEXICON_RU['one_sided_button']))
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['game_mode'] = 'one_sided'
        users[message.from_user.id]['total_games'] += 1
        users[message.from_user.id]['AI_map'] = create_map()
        users[message.from_user.id]['hits'] = []
        users[message.from_user.id]['attempts'] = ATTEMPTS
        users[message.from_user.id]['ships_left'] = SHIPS_LEFT
    else:
        await message.answer('Пока мы играем в игру я могу '
                             'реагировать только на нажатие кнопок на игровом поле '
                             'и команды /cancel и /stat')


# Этот хэндлер срабатывает на отказ пользователя играть в игру
@router.message(Text(text=LEXICON_RU['no_button']))
async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_RU['no'])


# Этот хэндлер срабатывает на выбор пользователя играть в игру против компьютера
@router.message(Text(text=LEXICON_RU['pair_AI_button']))
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=pair_AI_game_kb)
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['game_mode'] = 'pair_AI'
        users[message.from_user.id]['total_games'] += 1
        users[message.from_user.id]['AI_map'] = create_map()
        users[message.from_user.id]['hits'] = []
        users[message.from_user.id]['tiles'] = []
        users[message.from_user.id]['tiles_left'] = TILES_LEFT
        users[message.from_user.id]['ships_left'] = SHIPS_LEFT
        users[message.from_user.id]['player_map'] = player_map()
        users[message.from_user.id]['player_ships'] = {}
    else:
        await message.answer('Пока мы играем в игру я могу '
                             'реагировать только на нажатие кнопок на игровом поле '
                             'и команды /cancel и /stat')