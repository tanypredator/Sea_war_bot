from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon_ru import LEXICON_RU, HIT_BUTTON_SYMBOLS

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
    coords = f'AI,{x+1},{y+1}'
    keyboard[y][x] = InlineKeyboardButton(
        text=HIT_BUTTON_SYMBOLS[status],
        callback_data=coords)
    rebuilt_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=keyboard,
                                                                  resize_keyboard=True)
    return rebuilt_keyboard
