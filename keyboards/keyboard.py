from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUser
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

# ------- Создаем клавиатуру через ReplyKeyboardBuilder -------

# Создаем кнопки с ответами согласия и отказа
button_yes: KeyboardButton = KeyboardButton(text=LEXICON_RU['yes_button'])
button_no: KeyboardButton = KeyboardButton(text=LEXICON_RU['no_button'])

# Инициализируем билдер для клавиатуры с кнопками "Давай" и "Не хочу!"
yes_no_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с параметром width=2
yes_no_kb_builder.row(button_yes, button_no, width=2)

# Создаем клавиатуру с кнопками "Давай!" и "Не хочу!"
yes_no_kb = yes_no_kb_builder.as_markup(
                                one_time_keyboard=True,
                                resize_keyboard=True)


# ------- Создаем клавиатуру через ReplyKeyboardBuilder -------

# Создаем кнопки с ответами согласия и отказа
button_one_sided: KeyboardButton = KeyboardButton(text=LEXICON_RU['one_sided_button'])
button_pair_AI: KeyboardButton = KeyboardButton(text=LEXICON_RU['pair_AI_button'])
button_pair_human: KeyboardButton = KeyboardButton(text=LEXICON_RU['pair_human_button'])

# Инициализируем билдер для клавиатуры с кнопками режима игры
game_mode_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с параметром width=3
game_mode_kb_builder.row(button_one_sided, button_pair_AI, button_pair_human, width=3)

# Создаем клавиатуру с кнопками "Давай!" и "Не хочу!"
game_mode_kb = game_mode_kb_builder.as_markup(
                                one_time_keyboard=True,
                                resize_keyboard=True)


button_choose_enemy: KeyboardButton = KeyboardButton(
            text="Выбрать противника",
            request_user=KeyboardButtonRequestUser(request_id=1))

choose_enemy_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

choose_enemy_kb_builder.row(button_choose_enemy)

choose_enemy_kb = choose_enemy_kb_builder.as_markup(
                                one_time_keyboard=True,
                                resize_keyboard=True)
