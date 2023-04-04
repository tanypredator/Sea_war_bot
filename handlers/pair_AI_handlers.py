from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery

from keyboards.keyboard import yes_no_kb, game_mode_kb
from keyboards.pair_AI_keyboard import rebuild_keyboard
from lexicon.lexicon_ru import LEXICON_RU
from services.sea_war import create_map, shot_result, player_ship_placement
from User_dict.user_dict import users

router: Router = Router()


# Этот хэндлер срабатывает на любую из игровых кнопок
@router.callback_query(lambda callback: users[callback.from_user.id]['game_mode'] == 'pair_AI', Text(text=[str(i)+','+str(j) for i in range(1,9) for j in range(1,9)]))
async def process_game_button(callback: CallbackQuery):
    coords = callback.data.split(',')
    coord_y = int(coords[0]) - 1
    coord_x = int(coords[1]) - 1
    if [coord_y, coord_x] not in users[callback.from_user.id]['tiles'] and users[callback.from_user.id]['tiles_left'] > 0:
        status = 'place'
        users[callback.from_user.id]['tiles_left'] -= 1
        users[callback.from_user.id]['player_map'][coord_y][coord_x] = 1
        users[callback.from_user.id]['tiles'].append([coord_y, coord_x])
        await callback.message.edit_text(
        text=f"{LEXICON_RU['tiles left']} = {users[callback.from_user.id]['tiles_left']}", reply_markup=rebuild_keyboard(callback.message.reply_markup.inline_keyboard, coord_x, coord_y, status))
    elif [coord_y, coord_x] in users[callback.from_user.id]['tiles']:
        status = 'empty'
        users[callback.from_user.id]['tiles_left'] += 1
        users[callback.from_user.id]['player_map'][coord_y][coord_x] = 0
        users[callback.from_user.id]['tiles'].remove([coord_y, coord_x])
        await callback.message.edit_text(
        text=f"{LEXICON_RU['tiles left']} = {users[callback.from_user.id]['tiles_left']}", reply_markup=rebuild_keyboard(callback.message.reply_markup.inline_keyboard, coord_x, coord_y, status))
    
    
    if users[callback.from_user.id]['tiles_left'] == 0:
    	result = player_ship_placement(users[callback.from_user.id]['player_ships'], users[callback.from_user.id]['player_map'])[0]
    	users[callback.from_user.id]['player_ships'] = player_ship_placement(users[callback.from_user.id]['player_ships'], users[callback.from_user.id]['player_map'])[0]

    await callback.answer()
