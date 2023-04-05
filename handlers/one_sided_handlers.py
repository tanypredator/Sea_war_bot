from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery

from keyboards.keyboard import yes_no_kb, game_mode_kb
from keyboards.keyboard_map import rebuild_keyboard
from lexicon.lexicon_ru import LEXICON_RU
from services.sea_war import shot_result
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
    user = users[callback.from_user.id]
    user['attempts'] -= 1
    play_map = user['AI_map']
    hits = user['hits']
    result = shot_result(play_map[0], play_map[1], hits, coord_x, coord_y)
    if result == 'killed':
    	user['ships_left'] -= 1
    if user['ships_left'] == 0:
        await callback.message.edit_text(
        text=LEXICON_RU['user_won'],
        reply_markup=None)
        user['wins'] += 1
        user['in_game'] = False
        await callback.message.answer(text=LEXICON_RU['new_game'], reply_markup=game_mode_kb)
    elif user['attempts'] == 0:
       await callback.message.edit_text(
        text=LEXICON_RU['user_failed'],
       reply_markup=None)
       user['in_game'] = False
       await callback.message.answer(text=LEXICON_RU['new_game'], reply_markup=game_mode_kb)
    else:
        await callback.message.edit_text(
        text=LEXICON_RU[result], reply_markup=rebuild_keyboard(callback.message.reply_markup.inline_keyboard, coord_x, coord_y, result))
    await callback.answer(text = f"{LEXICON_RU['shots left']} = {user['attempts']}")
