from datetime import datetime
import sqlite3


async def connect_to_db():
    conn = sqlite3.connect('db/birthdays.db')
    return conn


async def save_birthday_to_db(user_id, birthday):
    conn = await connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (id, birthday, receive_notifications) VALUES (?, ?, 1)",
                   (user_id, birthday.strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()


async def get_birthday_from_db(user_id):
    conn = await connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT birthday FROM users WHERE id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return datetime.strptime(result[0], "%Y-%m-%d").date()
    else:
        return None


async def delete_birthday_from_db(user_id):
    conn = await connect_to_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
