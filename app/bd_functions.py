from datetime import datetime


def days_until_birthday(birthdate):
    today = datetime.now()
    next_birthday = datetime(today.year, birthdate.month, birthdate.day)
    if today.date() > next_birthday.date():
        next_birthday = datetime(today.year + 1, birthdate.month, birthdate.day)
    days_until = (next_birthday - today).days
    return days_until


def days_after_birthday(birthday: datetime) -> int:
    today = datetime.now().date()
    next_birthday = datetime(today.year, birthday.month, birthday.day).date()
    if next_birthday <= today:
        next_birthday = datetime(today.year + 1, birthday.month, birthday.day).date()
    days_after = (today - next_birthday).days + 365
    return days_after
