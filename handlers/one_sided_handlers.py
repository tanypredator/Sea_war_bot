from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery

from keyboards.keyboard import yes_no_kb, game_mode_kb
from keyboards.keyboard_map import rebuild_keyboard
from lexicon.lexicon_ru import LEXICON_RU
from services.sea_war import create_map, shot_result
from User_dict.user_dict import users

router: Router = Router()
ATTEMPTS: int = 40
SHIPS_LEFT: int = 7


# Этот хэндлер срабатывает на любую из игровых кнопок
@router.callback_query(lambda callback: users[callback.from_user.id]['game_mode'] == 'one_sided', Text(text=[str(i)+','+str(j) for i in range(1,9) for j in range(1,9)]))
async def process_game_button(callback: CallbackQuery):
    coords = callback.data.split(',')
    coord_y = int(coords[0]) - 1
    coord_x = int(coords[1]) - 1
    users[callback.from_user.id]['attempts'] -= 1
    play_map = users[callback.from_user.id]['AI_map']
    hits = users[callback.from_user.id]['hits']
    result = shot_result(play_map, hits, coord_x, coord_y)
    if result == 'killed':
    	users[callback.from_user.id]['ships_left'] -= 1
    if users[callback.from_user.id]['ships_left'] == 0:
        await callback.message.edit_text(
        text=LEXICON_RU['user_won'],
        reply_markup=None)
        users[callback.from_user.id]['wins'] += 1
        users[callback.from_user.id]['in_game'] = False
        await callback.message.answer(text=LEXICON_RU['new_game'], reply_markup=yes_no_kb)
    elif users[callback.from_user.id]['attempts'] == 0:
       await callback.message.edit_text(
        text=LEXICON_RU['user_failed'],
       reply_markup=None)
       users[callback.from_user.id]['in_game'] = False
       await callback.message.answer(text=LEXICON_RU['new_game'], reply_markup=yes_no_kb)
    else:
        await callback.message.edit_text(
        text=LEXICON_RU[result], reply_markup=rebuild_keyboard(callback.message.reply_markup.inline_keyboard, coord_x, coord_y, result))
    await callback.answer(text = f"{LEXICON_RU['shots left']} = {users[callback.from_user.id]['attempts']}")
