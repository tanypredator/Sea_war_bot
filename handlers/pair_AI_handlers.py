from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery

from keyboards.keyboard import yes_no_kb, game_mode_kb
from keyboards.pair_AI_keyboard import player_keyboard_rebuild, player_keyboard_restore
from keyboards.keyboard_map import game_kb, rebuild_keyboard
from lexicon.lexicon_ru import LEXICON_RU
from services.sea_war import create_AI_map, shot_result, player_ship_placement
from User_dict.user_dict import users

router: Router = Router()


# Этот хэндлер срабатывает на любую из игровых кнопок
@router.callback_query(lambda callback: users[callback.from_user.id]['game_mode'] == 'pair_AI', Text(text=[str(i)+','+str(j) for i in range(1,9) for j in range(1,9)]))
async def process_game_button(callback: CallbackQuery):
    coords = callback.data.split(',')
    coord_y = int(coords[0]) - 1
    coord_x = int(coords[1]) - 1
    user = users[callback.from_user.id]
    if [coord_y, coord_x] not in user['tiles'] and user['tiles_left'] > 0:
        status = 'place'
        user['tiles_left'] -= 1
        user['player_map'][coord_y][coord_x] = 1
        user['tiles'].append([coord_y, coord_x])
        await callback.message.edit_text(
        text=f"{LEXICON_RU['tiles left']} = {user['tiles_left']}", reply_markup=player_keyboard_rebuild(callback.message.reply_markup.inline_keyboard, coord_x, coord_y, status))
    elif [coord_y, coord_x] in user['tiles']:
        status = 'empty'
        user['tiles_left'] += 1
        user['player_map'][coord_y][coord_x] = 0
        user['tiles'].remove([coord_y, coord_x])
        await callback.message.edit_text(
        text=f"{LEXICON_RU['tiles left']} = {user['tiles_left']}", reply_markup=player_keyboard_rebuild(callback.message.reply_markup.inline_keyboard, coord_x, coord_y, status))
    
    if user['tiles_left'] == 0:
        await callback.message.edit_text(
        text=LEXICON_RU['no_tiles_left'], reply_markup=callback.message.reply_markup)

    await callback.answer()


# Этот хэндлер срабатывает на подтверждение расположения кораблей 
@router.callback_query(Text(text='confirm_placement'))
async def confirm_placement(callback: CallbackQuery):
    user = users[callback.from_user.id]
    result = player_ship_placement(user['player_ships'], user['player_map'])[0]
    user['player_ships'] = player_ship_placement(user['player_ships'], user['player_map'])[0]
    
    if result == "ship too long":
        await callback.message.edit_text(text=LEXICON_RU['ship_too_long'], reply_markup=player_keyboard_restore())
    
    elif result == "diagonal placement":
        await callback.message.edit_text(	text=LEXICON_RU['diagonal_placement'], reply_markup=player_keyboard_restore())
   
    elif result == "wrong placement":
        await callback.message.edit_text(	text=LEXICON_RU['wrong_placement'], reply_markup=player_keyboard_restore())
    
    elif result == "placement confirmed":
        await callback.message.edit_text(	text=LEXICON_RU['placement_confirmed'], reply_markup=game_kb)
    
    await callback.answer()
