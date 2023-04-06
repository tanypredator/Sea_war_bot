from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery

from keyboards.keyboard import game_mode_kb

from keyboards.player_map_keyboard import player_keyboard_rebuild, player_game_kb, player_map_restore

from keyboards.keyboard_AI_pair import AI_pair_game_kb, rebuild_keyboard

from lexicon.lexicon_ru import LEXICON_RU
from services.sea_war import create_AI_map, shot_result, player_ship_placement
from User_dict.user_dict import users

router: Router = Router()


# Этот хэндлер срабатывает на кнопки при размещении корабля
@router.callback_query(Text(text=[str(i)+','+str(j) for i in range(1,9) for j in range(1,9)]))
async def process_game_button(callback: CallbackQuery):
    coords = callback.data.split(',')
    coord_y = int(coords[0])
    coord_x = int(coords[1])
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
    print(users.keys())
    for row in user['player_map']:
        print(row)
    print(user['player_ships'])
    result = player_ship_placement(user['player_ships'], user['player_map'])[0]
    print(user['player_ships'])
    
    if result == "ship too long":
        user['tiles_left'] = 13
        user['player_map'] = player_map_restore(user['player_map'], user['tiles'])[0]
        user['tiles'] = player_map_restore(user['player_map'], user['tiles'])[1]
        await callback.message.edit_text(text=LEXICON_RU['ship_too_long'], reply_markup=player_game_kb)
    
    elif result == "diagonal placement":
        user['tiles_left'] = 13
        user['player_map'] = player_map_restore(user['player_map'], user['tiles'])[0]
        user['tiles'] = player_map_restore(user['player_map'], user['tiles'])[1]
        await callback.message.edit_text(	text=LEXICON_RU['diagonal_placement'], reply_markup=player_game_kb)
   
    elif result == "wrong placement":
        user['tiles_left'] = 13
        user['player_map'] = player_map_restore(user['player_map'], user['tiles'])[0]
        user['tiles'] = player_map_restore(user['player_map'], user['tiles'])[1]
        await callback.message.edit_text(	text=LEXICON_RU['wrong_placement'], reply_markup=player_game_kb)
    
    elif result == "placement confirmed":
        user['player_ships'] = player_ship_placement(user['player_ships'], user['player_map'])[1]
        print(user['player_ships'])
        # TO DO
        user['player_kb'] = save_player_kb(callback.message.reply_markup.inline_keyboard)
        await callback.message.edit_text(	text=LEXICON_RU['placement_confirmed'], reply_markup=AI_pair_game_kb)
    
    await callback.answer()


# Этот хэндлер срабатывает на команду "/cancel"
@router.callback_query(Text(text='/cancel'))
async def cancel_inline(callback: CallbackQuery):
    user = users[callback.from_user.id]
    if user['in_game']:
        await callback.message.edit_text(text ='Вы вышли из игры. Если захотите сыграть '
                             'снова - выберите режим игры', reply_markup=player_game_kb)
        user['in_game'] = False
    else:
        await callback.message.edit_text(text ='А мы и так с вами не играем. '
                             'Может, сыграем разок?', reply_markup=game_mode_kb)

        await callback.answer()


# Этот хэндлер срабатывает на кнопки стрельбы по карте компьютерного игрока
@router.callback_query(Text(text=['AI_pair,'+str(i)+','+str(j) for i in range(1,9) for j in range(1,9)]))
async def process_AI_pair_button(callback: CallbackQuery):
    coords = callback.data.split(',')
    coord_y = int(coords[1])
    coord_x = int(coords[2])
    user = users[callback.from_user.id]
    play_map = user['AI_map']
    for row in play_map[0]:
    	print(row)
    hits = user['player_hits']
    print(coord_x, coord_y)
    result = shot_result(play_map[0], play_map[1], hits, coord_x, coord_y)
    print(result)
    if result == 'killed':
    	user['AI_ships_left'] -= 1
    if user['AI_ships_left'] == 0:
        await callback.message.edit_text(
        text=LEXICON_RU['user_won'],
        reply_markup=None)
        user['wins'] += 1
        user['in_game'] = False
        await callback.message.answer(text=LEXICON_RU['new_game'], reply_markup=game_mode_kb)

    else:
        # TO DO
        user['enemy_kb'] = save_player_kb(callback.message.reply_markup.inline_keyboard)
        await callback.message.edit_text(
        text=LEXICON_RU[result], reply_markup=rebuild_keyboard_AI_pair(callback.message.reply_markup.inline_keyboard, coord_x, coord_y, result))
    await callback.answer(text = f"{LEXICON_RU['shots left']} = {user['attempts']}")


# Этот хэндлер срабатывает на кнопку перехода к следующему ходу
@router.callback_query(Text(text='next_move'))
async def confirm_placement(callback: CallbackQuery):
    
    user = users[callback.from_user.id]
    AI_shot =AI_shot(user['AI_tiles_for_shot'], user['AI_hits'], (user['player_map'], user['player_ships'])
    user['AI_tiles_for_shot'] = AI_shot[3]
    user['AI_hits'] = AI_shot[4]
    
