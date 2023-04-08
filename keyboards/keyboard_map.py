from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon_ru import LEXICON_RU

# ------- Создаем игровую клавиатуру без использования билдера -------


# Создаем объекты инлайн-кнопок
buttons: list[InlineKeyboardButton] = []

keyboard: list[list[InlineKeyboardButton]] = []

for i in range(1, 9):
    for j in range(1, 9):
        buttons.append(InlineKeyboardButton(
            text='*',
            callback_data=f'AI,{i},{j}'))
        if not j % 8:
            keyboard.append(buttons)
            buttons = []

# Создаем игровую клавиатуру с нумерованными кнопками как список списков

game_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=keyboard,
    resize_keyboard=True)


# Пересоздаем клавиатуру после нажатия кнопки

def rebuild_keyboard(old_board, x, y, status):
    keyboard = old_board
    # because keyboard indices are from 0...
    x -= 1
    y -= 1
    coords = f'AI,{x},{y}'
    if status == "miss":
        keyboard[y][x] = InlineKeyboardButton(
            text='🌊',
            callback_data=coords)
    elif status == "hit":
        keyboard[y][x] = InlineKeyboardButton(
            text='💥',
            callback_data=coords)
    elif status == "killed":
        keyboard[y][x] = InlineKeyboardButton(
            text='💥',
            callback_data=coords)
    elif status == "mermaid":
        keyboard[y][x] = InlineKeyboardButton(
            text='🧜‍♀',
            callback_data=coords)
    elif status == "squid":
        keyboard[y][x] = InlineKeyboardButton(
            text='🦑',
            callback_data=coords)
    elif status == "shark":
        keyboard[y][x] = InlineKeyboardButton(
            text='🦈',
            callback_data=coords)
    elif status == "dragon":
        keyboard[y][x] = InlineKeyboardButton(
            text='🐉',
            callback_data=coords)
    elif status == "boat":
        keyboard[y][x] = InlineKeyboardButton(
            text='⛵️',
            callback_data=coords)
    elif status == "island":
        keyboard[y][x] = InlineKeyboardButton(
            text='🏝',
            callback_data=coords)
    elif status == "volcano":
        keyboard[y][x] = InlineKeyboardButton(
            text='🌋',
            callback_data=coords)
    rebuilt_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=keyboard,
                                                                  resize_keyboard=True)
    return rebuilt_keyboard
