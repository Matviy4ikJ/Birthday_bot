from app.db_funtions import save_birthday_to_db, get_birthday_from_db, delete_birthday_from_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
import sqlite3

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.bd_functions import days_until_birthday, days_after_birthday
import app.keyboard as keyb
from datetime import datetime

router = Router()

scheduler = AsyncIOScheduler()


class Datadate(StatesGroup):
    date_change = State()


@router.message(CommandStart())
async def register(message: Message, state: FSMContext):
    await state.set_state(Datadate.date_change)
    await message.answer('Привіт! Введи дату свого народження в форматі ДД/ММ/РР')


@router.message(Datadate.date_change)
async def get_date(message: Message, state: FSMContext):
    while True:
        try:
            await state.update_data(date=message.text)
            data = await state.get_data()
            date_string = data['date']
            birthday = datetime.strptime(date_string, '%d/%m/%y')
            user_id = message.from_user.id
            await save_birthday_to_db(user_id, birthday)
            days_until = days_until_birthday(birthday)
            break

        except ValueError:
            await message.answer('Неправильний формат. Введи дату в форматі ДД/ММ/РР. Для прикладу 29/08/10')
            return

    await message.answer(f'До твого дня народження залишилося {days_until} днів!', reply_markup=keyb.main,
                         one_time_keyboard=False)
    await state.clear()


@router.message(F.text == 'До Д.Р')
async def until_birthday(message: Message):
    user_id = message.from_user.id
    birthday = await get_birthday_from_db(user_id)
    days_until = days_until_birthday(birthday)
    if days_until == 0:
        await message.answer('Твій день народження сьогодні! Вітаю!')
    else:
        await message.answer(f'До вашого дня народження залишилося {days_until} днів!')


@router.message(F.text == 'Після Д.Р')
async def after_birthday(message: Message):
    user_id = message.from_user.id
    birthday = await get_birthday_from_db(user_id)
    days_after = days_after_birthday(birthday)
    if days_after == 0:
        await message.answer('Твій день народження сьогодні! Вітаю!')
    else:
        await message.answer(f'Після вашого дня народження пройшло {days_after} днів!')


@router.message(F.text == 'Змінити дату')
async def change_birthday(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await delete_birthday_from_db(user_id)
    await message.answer("Введіть нову дату свого народження в форматі ДД/ММ/РР")
    await state.set_state(Datadate.date_change)


@router.message(Datadate.date_change)
async def change_birthday(message: Message, state: FSMContext):
    while True:
        try:
            await state.update_data(date=message.text)
            data = await state.get_data()
            date_string = data['date']
            new_birthday = datetime.strptime(date_string, '%d/%m/%y')
            user_id = message.from_user.id
            await delete_birthday_from_db(user_id)
            await save_birthday_to_db(user_id, new_birthday)
            days_until = days_until_birthday(new_birthday)
            break

        except ValueError:
            await message.answer('Неправильний формат. Введи дату в форматі ДД/ММ/РР. Для прикладу 29/08/10')
            return

    await message.answer(f'До вашого дня народження залишилося {days_until} днів!')
    await state.clear()


@router.message(F.text == 'Увімкнути сповіщення')
async def enable_notifications(message: Message):
    conn = sqlite3.connect('db/birthdays.db')
    cursor = conn.cursor()
    user_id = message.from_user.id
    cursor.execute('UPDATE users SET receive_notifications = 1 WHERE id = ?', (user_id,))
    conn.commit()
    await message.reply('Сповіщення про дні народження увімкнуті')


@router.message(F.text == 'Вимкнути сповіщення')
async def disable_notifications(message: Message):
    conn = sqlite3.connect('db/birthdays.db')
    cursor = conn.cursor()
    user_id = message.from_user.id
    cursor.execute('UPDATE users SET receive_notifications = 0 WHERE id = ?', (user_id,))
    conn.commit()
    await message.reply('Сповіщення про дні народження вимкнуті')
