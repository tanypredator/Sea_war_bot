from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon_ru import LEXICON_RU


# ------- Создаем игровую клавиатуру без использования билдера -------


# Создаем объекты инлайн-кнопок
buttons: list[InlineKeyboardButton] = []

keyboard: list[list[InlineKeyboardButton]] = []

for i in range(1, 9):
    for j in range(1, 9):
        buttons.append(InlineKeyboardButton(
        text = '🌊',
        callback_data=f'{i},{j}'))
        if not j % 8:
            keyboard.append(buttons)
            buttons = []

confirm_buttons = []
confirm_buttons.append(InlineKeyboardButton(
        text = LEXICON_RU['confirm_placement'],
        callback_data='confirm_placement'))
confirm_buttons.append(InlineKeyboardButton(
        text = LEXICON_RU['/cancel'],
        callback_data='/cancel'))

keyboard.append(confirm_buttons)

# Создаем игровую клавиатуру с нумерованными кнопками как список списков

player_game_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
                                    inline_keyboard=keyboard,
                                  resize_keyboard=True)


# Пересоздаем клавиатуру после нажатия кнопки
def player_keyboard_rebuild(old_board, x, y, status):
	keyboard = old_board
	x -= 1
	y -= 1
	if status == "empty":
		keyboard[y][x] = InlineKeyboardButton(
        text = '🌊',
        callback_data=f'{y},{x}')
	elif status == "place":
		keyboard[y][x] = InlineKeyboardButton(
        text = '🔲',
        callback_data=f'{y},{x}')
	rebuilt_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup( inline_keyboard=keyboard,
                                  resize_keyboard=True)
	return rebuilt_keyboard


def player_map_restore(player_map: list[list], tiles: list[list]):
	for tile in tiles:
		y = tile[0]
		x = tile[1]
		player_map[y][x] = 0
		tiles.remove(tile)
	return (player_map, tiles)