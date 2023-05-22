from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery
import asyncio
from aiogram import Bot

from keyboards.keyboard import game_mode_kb

from keyboards.player_map_keyboard import player_map_restore, confirm_player_kb
from keyboards.human_pair_map_keyboard import human_pair_keyboard_rebuild, first_player_game_kb, second_player_game_kb, \
    hide_enemy_kb, rebuild_enemy_keyboard_human_pair

from keyboards.keyboard_AI_pair import rebuild_keyboard_AI_pair, rebuild_player_keyboard_AI_pair

from lexicon.lexicon_ru import LEXICON_RU
from services.sea_war import shot_result, player_ship_placement, AI_shot
from User_dict.user_dict import users, game_pairs

router: Router = Router()


# Этот хэндлер срабатывает на кнопки при размещении корабля
@router.callback_query(
    Text(text=['first_player' + ',' + str(i) + ',' + str(j) for i in range(1, 9) for j in range(1, 9)]))
@router.callback_query(
    Text(text=['second_player' + ',' + str(i) + ',' + str(j) for i in range(1, 9) for j in range(1, 9)]))
async def process_game_button(callback: CallbackQuery):
    coords = callback.data.split(',')
    player = coords[0]
    coord_y = int(coords[1])
    coord_x = int(coords[2])
    user = users[callback.from_user.id]
    # if the tile is not already marked, then mark it as a ship deck
    if [coord_y, coord_x] not in user['tiles'] and user['tiles_left'] > 0:
        status = 'place'
        user['tiles_left'] -= 1
        user['player_map'][coord_y][coord_x] = 1
        user['tiles'].append([coord_y, coord_x])
        await callback.message.edit_text(
            text=f"{LEXICON_RU['tiles left']} = {user['tiles_left']}",
            reply_markup=human_pair_keyboard_rebuild(callback.message.reply_markup.inline_keyboard, player, coord_x,
                                                     coord_y, status))

    # if the tile is already marked, then unmark it
    elif [coord_y, coord_x] in user['tiles']:
        status = 'empty'
        user['tiles_left'] += 1
        user['player_map'][coord_y][coord_x] = 0
        user['tiles'].remove([coord_y, coord_x])
        await callback.message.edit_text(
            text=f"{LEXICON_RU['tiles left']} = {user['tiles_left']}",
            reply_markup=human_pair_keyboard_rebuild(callback.message.reply_markup.inline_keyboard, player,
                                                     coord_x, coord_y, status))

    if user['tiles_left'] == 0:
        await callback.message.edit_text(
            text=LEXICON_RU['no_tiles_left'], reply_markup=callback.message.reply_markup)

    await callback.answer()


# Этот хэндлер срабатывает на подтверждение расположения кораблей
@router.callback_query(Text(text='first_player_confirm_placement'))
async def confirm_placement(callback: CallbackQuery, bot: Bot):
    user = users[callback.from_user.id]
    # check the player ship placement:
    placement_check = player_ship_placement(user['player_ships'], user['player_map'])
    result = placement_check[0]
    # and if it is wrong, restore the map and tiles to set:
    if result == "ship too long":
        user['player_ships'] = {}
        user['tiles_left'] = 13
        user['player_map'], user['tiles'] = player_map_restore(user['player_map'], user['tiles'])
        await callback.message.edit_text(text=LEXICON_RU['ship_too_long'], reply_markup=first_player_game_kb)

    elif result == "diagonal placement":
        user['player_ships'] = {}
        user['tiles_left'] = 13
        user['player_map'], user['tiles'] = player_map_restore(user['player_map'], user['tiles'])
        await callback.message.edit_text(text=LEXICON_RU['diagonal_placement'],
                                         reply_markup=first_player_game_kb)

    elif result == "wrong placement":
        user['player_ships'] = {}
        user['tiles_left'] = 13
        user['player_map'], user['tiles'] = player_map_restore(user['player_map'], user['tiles'])
        await callback.message.edit_text(text=LEXICON_RU['wrong_placement'],
                                         reply_markup=first_player_game_kb)

    elif result == "placement confirmed":
        print(user['player_ships'])
        # replace confirmation button with the next move button and make tiles inactive:
        user['player_kb'] = confirm_player_kb(user['player_map'])

        second_player_id = game_pairs[callback.from_user.id]['second_player']
        users[second_player_id]['enemy_kb'] = hide_enemy_kb(user['player_map'], 'first_player')
        users[second_player_id]['enemy_map'] = user['player_map']
        users[second_player_id]['enemy_ships'] = user['player_ships']
        await callback.answer(text=LEXICON_RU['wait_for_enemy'], reply_markup=user['player_kb'])
        enemy_confirmed = f"{LEXICON_RU['first_player_placed_ships']}"
        await bot.send_message(second_player_id, enemy_confirmed, reply_markup=second_player_game_kb)

    await callback.answer()


# Этот хэндлер срабатывает на подтверждение расположения кораблей
@router.callback_query(Text(text='second_player_confirm_placement'))
async def confirm_placement(callback: CallbackQuery, bot: Bot):
    print(callback.from_user.id, type(callback.from_user.id))
    user = users[callback.from_user.id]
    # check the player ship placement:
    placement_check = player_ship_placement(user['player_ships'], user['player_map'])
    result = placement_check[0]
    # and if it is wrong, restore the map and tiles to set:
    if result == "ship too long":
        user['player_ships'] = {}
        user['tiles_left'] = 13
        user['player_map'], user['tiles'] = player_map_restore(user['player_map'], user['tiles'])
        await callback.message.edit_text(text=LEXICON_RU['ship_too_long'], reply_markup=second_player_game_kb)

    elif result == "diagonal placement":
        user['player_ships'] = {}
        user['tiles_left'] = 13
        user['player_map'], user['tiles'] = player_map_restore(user['player_map'], user['tiles'])
        await callback.message.edit_text(text=LEXICON_RU['diagonal_placement'],
                                         reply_markup=second_player_game_kb)

    elif result == "wrong placement":
        user['player_ships'] = {}
        user['tiles_left'] = 13
        user['player_map'], user['tiles'] = player_map_restore(user['player_map'], user['tiles'])
        await callback.message.edit_text(text=LEXICON_RU['wrong_placement'],
                                         reply_markup=second_player_game_kb)

    elif result == "placement confirmed":
        print(user['player_ships'])
        # replace confirmation button with the next move button and make tiles inactive:
        user['player_kb'] = confirm_player_kb(user['player_map'])

        first_player_id = ''
        for first_user in game_pairs:
            if game_pairs[first_user]['second_player'] == callback.from_user.id:
                first_player_id = first_user

        users[first_player_id]['enemy_kb'] = hide_enemy_kb(user['player_map'], 'second_player')
        users[first_player_id]['enemy_map'] = user['player_map']
        users[first_player_id]['enemy_ships'] = user['player_ships']
        await callback.answer(text=LEXICON_RU['wait_for_enemy'], reply_markup=user['player_kb'])
        enemy_confirmed = f"{LEXICON_RU['placement_confirmed']}"
        await bot.send_message(first_player_id, enemy_confirmed, reply_markup=users[first_player_id]['enemy_kb'])

    await callback.answer()


# Этот хэндлер срабатывает на кнопки стрельбы по карте другого игрока
@router.callback_query(
    Text(text=['in-game,' + 'first_player' + ',' + str(i) + ',' + str(j) for i in range(1, 9) for j in range(1, 9)]))
@router.callback_query(
    Text(text=['in-game,' + 'second_player' + ',' + str(i) + ',' + str(j) for i in range(1, 9) for j in range(1, 9)]))
async def process_human_pair_button(callback: CallbackQuery, bot: Bot):
    user = users[callback.from_user.id]
    if user['shot_status'] == 'not_shot_yet':
        coords = callback.data.split(',')
        enemy_order = coords[1]
        coord_y = int(coords[2])
        coord_x = int(coords[3])

        enemy_map = user['enemy_map']
        enemy_ships = user['enemy_ships']
        player_hits = user['player_hits']

        enemy_id = ''
        if enemy_order == 'first_player':
            for first_user in game_pairs:
                if game_pairs[first_user]['second_player'] == callback.from_user.id:
                    enemy_id = first_user
        elif enemy_order == 'second_player':
            enemy_id = game_pairs[callback.from_user.id]['second_player']

        enemy = users[enemy_id]

        print('user:', callback.from_user.first_name, callback.from_user.id)
        print('enemy:', enemy_order, enemy_id)
        print('enemy_map', enemy_map)
        print("enemy_ships", enemy_ships)
        print("player_hits", player_hits)
        print('coord_x', coord_x)
        print('coord_y', coord_y)

        # check the result of player shot:
        result = shot_result(enemy_map, enemy_ships, player_hits, coord_x, coord_y)

        if result == 'killed':
            user['enemy_ships_left'] -= 1
            enemy['player_ships_left'] -= 1
        if user['enemy_ships_left'] == 0:
            await callback.message.edit_text(
                text=LEXICON_RU['user_won'],
                reply_markup=None)
            await bot.send_message(enemy_id, LEXICON_RU['user_failed'])
            user['wins'] += 1
            user['in_game'] = False
            enemy['in_game'] = False
            await callback.message.answer(text=LEXICON_RU['new_game'], reply_markup=game_mode_kb)
            await bot.send_message(enemy_id, LEXICON_RU['new_game'], reply_markup=game_mode_kb)

        else:
            user['enemy_kb'] = rebuild_enemy_keyboard_human_pair(callback.message.reply_markup.inline_keyboard,
                                                                 enemy_order, coord_x, coord_y, result)
            await callback.message.edit_text(
                text=LEXICON_RU[result], reply_markup=user['enemy_kb'])
        user['shot_status'] = 'already_shot'
    else:
        await callback.message.edit_text(
            text=LEXICON_RU['inactive_button'], reply_markup=callback.message.reply_markup)

    await callback.answer()


# Этот хэндлер срабатывает на кнопку перехода к следующему ходу
@router.callback_query(Text(text='next_move_AI'))
async def go_to_AI_move(callback: CallbackQuery):
    user = users[callback.from_user.id]
    user['shot_status'] = 'not_shot_yet'
    # go to player map:
    await callback.message.edit_text(text='Мой ход', reply_markup=user['player_kb'])
    await asyncio.sleep(2)
    AI_shot_result = AI_shot(user['AI_tiles_for_shot'], user['AI_hits'], user['player_map'], user['player_ships'])
    AI_x = AI_shot_result[0]
    AI_y = AI_shot_result[1]
    AI_result = AI_shot_result[2]
    user['AI_tiles_for_shot'] = AI_shot_result[3]
    user['AI_hits'] = AI_shot_result[4]
    user['player_kb'] = rebuild_player_keyboard_AI_pair(user['player_kb'].inline_keyboard,
                                                        AI_x, AI_y, AI_result)
    if AI_result == 'killed_player':
        user['player_ships_left'] -= 1
    if user['player_ships_left'] == 0:
        await callback.message.edit_text(
            text=LEXICON_RU['user_failed'],
            reply_markup=None)
        user['in_game'] = False
        await callback.message.answer(text=LEXICON_RU['new_game'], reply_markup=game_mode_kb)
    else:
        await callback.message.edit_text(text=LEXICON_RU[AI_result], reply_markup=user['player_kb'])

    await callback.answer()


# Этот хэндлер срабатывает на кнопку перехода к следующему ходу
@router.callback_query(Text(text='next_move_player'))
async def confirm_placement(callback: CallbackQuery):
    user = users[callback.from_user.id]
    # go to enemy map:
    await callback.message.edit_text(text='Ваш ход', reply_markup=user['enemy_kb'])
    await callback.answer()


# Этот хэндлер срабатывает на нажатие на неактивную кнопку карты игрока
@router.callback_query(Text(text=['inactive,' + str(i) + ',' + str(j) for i in range(1, 9) for j in range(1, 9)]))
async def note_inactive_button(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['inactive_button'], reply_markup=callback.message.reply_markup)

    await callback.answer()
