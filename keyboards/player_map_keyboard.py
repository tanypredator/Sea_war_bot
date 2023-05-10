from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon_ru import LEXICON_RU, HIT_BUTTON_SYMBOLS

# ------- Создаем игровую клавиатуру без использования билдера -------


# Создаем объекты инлайн-кнопок
buttons: list[InlineKeyboardButton] = []

keyboard: list[list[InlineKeyboardButton]] = []

for i in range(1, 9):
    for j in range(1, 9):
        buttons.append(InlineKeyboardButton(
            text='🌊',
            callback_data=f'{i},{j}'))
        if not j % 8:
            keyboard.append(buttons)
            buttons = []

confirm_buttons = []
confirm_buttons.append(InlineKeyboardButton(
    text=LEXICON_RU['confirm_placement'],
    callback_data='confirm_placement'))
confirm_buttons.append(InlineKeyboardButton(
    text=LEXICON_RU['/cancel'],
    callback_data='/cancel'))

keyboard.append(confirm_buttons)

# Создаем игровую клавиатуру с нумерованными кнопками как список списков

player_game_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=keyboard,
    resize_keyboard=True)


#  rebuild keyboard after ship deck placement
def player_keyboard_rebuild(old_board, x, y, status):
    keyboard = old_board
    x -= 1
    y -= 1
    keyboard[y][x] = InlineKeyboardButton(
        text=HIT_BUTTON_SYMBOLS[status],
        callback_data=f'{y + 1},{x + 1}')
    rebuilt_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=keyboard,
                                                                  resize_keyboard=True)
    return rebuilt_keyboard


# remove previously chosen tiles from map and list of tiles
def player_map_restore(player_map: list[list], tiles: list[list]):
    for tile in tiles[:]:
        y, x = tile
        player_map[y][x] = 0
        tiles.remove(tile)
    return (player_map, tiles)


# change confirmation button to the next move button and make tiles inactive
def confirm_player_kb(player_map):
    in_game_buttons: list[InlineKeyboardButton] = []
    in_game_keyboard: list[list[InlineKeyboardButton]] = []
    for y in range(1, 9):
        for x in range(1, 9):
            if player_map[y][x] == 1:
                in_game_buttons.append(InlineKeyboardButton(
                    text='🔲',
                    callback_data=f'inactive,{y},{x}'))
            else: in_game_buttons.append(InlineKeyboardButton(
                    text='🌊',
                    callback_data=f'inactive,{y},{x}'))
            if not x % 8:
                in_game_keyboard.append(in_game_buttons)
                in_game_buttons = []

    next_move_player_button = [InlineKeyboardButton(
        text=LEXICON_RU['next_move'],
        callback_data='next_move_player'), InlineKeyboardButton(
        text=LEXICON_RU['/cancel'],
        callback_data='/cancel')]
    in_game_keyboard.append(next_move_player_button)

    in_game_player_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=in_game_keyboard,
                                                                   resize_keyboard=True)

    return in_game_player_kb
