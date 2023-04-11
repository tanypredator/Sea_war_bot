from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery
from aiogram import Bot

from keyboards.keyboard import yes_no_kb, game_mode_kb, choose_enemy_kb
from keyboards.keyboard_map import game_kb, rebuild_keyboard
from keyboards.player_map_keyboard import player_game_kb
from lexicon.lexicon_ru import LEXICON_RU
from services.sea_war import create_AI_map, shot_result, player_map, get_AI_tiles_for_shot
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
        'shot_status': None,
                                       'AI_map': None,
                                       'player_map': None,
                                       'attempts': None,
                                       'AI_ships_left': None,
                                       'player_hits': None,
                                       'tiles_left': None,
                                       'tiles': None,
                                       'AI_tiles_for_shot': None,
                                       'AI_hits': None,
                                       'player_ships_left': None,
                                       'player_kb': None,
                                       'enemy_kb': None,
                                       'enemy_id': None,
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
        await message.answer(text=LEXICON_RU['cancel_in_game'])
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer(text =LEXICON_RU['cancel_out_of_game'], reply_markup=game_mode_kb)


# Этот хэндлер срабатывает на инлайн кнопку "cancel"
@router.callback_query(Text(text='/cancel'))
async def cancel_inline(callback: CallbackQuery):
    user = users[callback.from_user.id]
    if user['in_game']:
        await callback.message.edit_text(text =LEXICON_RU['cancel_in_game'], reply_markup=None)
        user['in_game'] = False
        await callback.message.answer(text=LEXICON_RU['new_game'], reply_markup=game_mode_kb)
    else:
        await callback.message.edit_text(text =LEXICON_RU['cancel_out_of_game'],  reply_markup=None)
        await callback.message.answer(text=LEXICON_RU['new_game'], reply_markup=game_mode_kb)

        await callback.answer()


# Этот хэндлер срабатывает на выбор пользователя играть в игру без своего поля
@router.message(Text(text=LEXICON_RU['one_sided_button']))
async def one_sided_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)
    user = users[message.from_user.id]
    if not user['in_game']:
        user['in_game'] = True
        user['total_games'] += 1
        user['AI_map'] = create_AI_map()
        user['player_hits'] = []
        user['attempts'] = ATTEMPTS
        user['AI_ships_left'] = SHIPS_LEFT
    else:
        await message.answer(LEXICON_RU['choice_in_game'])


# Этот хэндлер срабатывает на выбор пользователя играть в игру против компьютера
@router.message(Text(text=LEXICON_RU['pair_AI_button']))
async def pair_AI_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=player_game_kb)
    user = users[message.from_user.id]
    if not user['in_game']:
        AI_tiles = get_AI_tiles_for_shot()
        user['in_game'] = True
        user['shot_status'] = 'not_shot_yet'
        user['total_games'] += 1
        user['AI_map'] = create_AI_map()
        user['player_hits'] = []
        user['tiles'] = []
        user['AI_tiles_for_shot'] = AI_tiles
        user['AI_hits'] = []
        user['tiles_left'] = TILES_LEFT
        user['AI_ships_left'] = SHIPS_LEFT
        user['player_ships_left'] = SHIPS_LEFT
        user['player_map'] = player_map()
        user['player_ships'] = {}
    else:
        await message.answer(LEXICON_RU['choice_in_game'])


# Этот хэндлер срабатывает на выбор пользователя играть в игру против человека
@router.message(Text(text=LEXICON_RU['pair_human_button']))
async def pair_AI_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=choose_enemy_kb)
    user = users[message.from_user.id]
    if not user['in_game']:
        AI_tiles = get_AI_tiles_for_shot()
        user['in_game'] = True
        user['shot_status'] = 'not_shot_yet'
        user['total_games'] += 1
        user['AI_map'] = create_AI_map()
        user['player_hits'] = []
        user['tiles'] = []
        user['AI_tiles_for_shot'] = AI_tiles
        user['AI_hits'] = []
        user['tiles_left'] = TILES_LEFT
        user['AI_ships_left'] = SHIPS_LEFT
        user['player_ships_left'] = SHIPS_LEFT
        user['player_map'] = player_map()
        user['player_ships'] = {}
    else:
        await message.answer(LEXICON_RU['choice_in_game'])


@router.message(lambda message: message.user_shared)
async def send_invite(message: Message, bot: Bot):
    await bot.send_message(message.user_shared.user_id, "test message")
    print(
        f"Request {message.user_shared.request_id}. "
        f"User ID: {message.user_shared.user_id}"
    )