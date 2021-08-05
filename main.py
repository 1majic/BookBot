import dbHelp
import YandexDisk as yd
import Keybord
from os import remove
from math import ceil

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InputFile, ParseMode

API_TOKEN = ""

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Введите книгу в формате ***("название")*** или ***(#номер)*** книги.', parse_mode=ParseMode.MARKDOWN, reply_markup=Keybord.main_kb)


@dp.message_handler(lambda message: message.text.startswith('"') and message.text.endswith('"'))
async def NameSearching(message: types.Message):
    try:
        name, rating, rewiew, num = dbHelp.FindByName('books', message.text[1:-1])[0]
        await message.answer(f"{name}\n{rating}\n\n{rewiew}\n{num}")
        yd.downloadFile(f'books/{name}.fb2')
        print(message.from_user.id)
        with open(f"{name}.fb2", 'rb') as file:
            await bot.send_document(message.from_user.id, (f"{name}.fb2", file))
        remove(f"{name}.fb2")
    except IndexError:
        await message.answer("Такой книги - нет!")


@dp.message_handler(lambda message: message.text.startswith('#'))
async def NameSearching(message: types.Message):
    try:
        name, rating, rewiew, num = dbHelp.FindById('books', message.text[1:-1])[0]
        await message.answer(f"{name}\n{rating}\n\n{rewiew}\n{num}")
        yd.downloadFile(f'books/{name}.fb2')
        print(message.from_user.id)
        with open(f"{name}.fb2", 'rb') as file:
            await bot.send_document(message.from_user.id, (f"{name}.fb2", file))
        remove(f"{name}.fb2")
    except IndexError:
        await message.answer("Такой книги - нет!")


@dp.message_handler(lambda message: message.text == "Случайная книга")
async def RandomBook(message: types.Message):
    name, rating, rewiew, num = dbHelp.LastId("books")
    await message.answer(f"{name}\n{rating}\n\n{rewiew}\n{num}")


@dp.message_handler(lambda message: message.text == "Список всех книг")
async def ListOfAllBooks(message: types.Message):
    books_name = yd.getBooks()
    pages = ceil(len(books_name) / 10)
    current_page = 1
    for i in range(len(books_name)):
        books_name[i] = f"{i+1}. **{books_name[i].replace('_', '** - ___')}___"
    if pages > 1:
        if 1 < current_page < pages:
            keybord = Keybord.book_list
        elif 1 < current_page == pages:
            keybord = Keybord.back_book_list
        elif pages > current_page == 1:
            keybord = Keybord.next_book_list
        await message.answer(f'Страница {current_page}/{pages}' + '\n\n' + '\n'.join(books_name[current_page * 10 - 10:current_page * 10]), reply_markup=keybord, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer("\n".join(books_name[current_page * 10 - 10:current_page * 10]))






@dp.message_handler()
async def UnknownCommand(message: types.Message):
    await message.answer("Неизвестная команда")


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)

# @dp.message_handler(lambda message: message.text)
# async def
