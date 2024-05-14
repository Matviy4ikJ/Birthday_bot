import sqlite3
import asyncio
from datetime import datetime
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from settings import token


conn = sqlite3.connect('db/birthdays.db')
cursor = conn.cursor()


bot = Bot(token)
scheduler = AsyncIOScheduler()


async def scheduled_message():
    cursor.execute("SELECT id, birthday, receive_notifications FROM users")
    users = cursor.fetchall()
    for user_id, birthday_str, receive_notifications in users:
        if receive_notifications:
            birthday = datetime.strptime(birthday_str, "%Y-%m-%d")
            current_date = datetime.now()
            next_birthday = datetime(current_date.year, birthday.month, birthday.day)

            if next_birthday < current_date:
                next_birthday = datetime(current_date.year + 1, birthday.month, birthday.day)

            days_until_birthday = (next_birthday - current_date).days
            message_text = f"До вашого дня народження залишилося {days_until_birthday} днів."
            await bot.send_message(user_id, message_text)

scheduler.add_job(scheduled_message, 'cron', hour=0)
scheduler.start()

asyncio.get_event_loop().run_forever()
