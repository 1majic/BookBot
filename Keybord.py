from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

button_randomBook = KeyboardButton('Случайная книга')
button_list = KeyboardButton('Список всех книг')

button_next_list = InlineKeyboardButton('Вперед', callback_data='next_list')
button_back_list = InlineKeyboardButton('Назад', callback_data='back_list')
next_book_list = InlineKeyboardMarkup().add(button_next_list)
back_book_list = InlineKeyboardMarkup().add(button_back_list)
book_list = InlineKeyboardMarkup().add(button_back_list).add(button_next_list)

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.row(button_randomBook, button_list)