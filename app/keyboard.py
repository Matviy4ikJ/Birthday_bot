from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Після Д.Р')],
                                     [KeyboardButton(text='До Д.Р')],
                                     [KeyboardButton(text='Змінити дату')],
                                     [KeyboardButton(text='Вимкнути сповіщення'),
                                      KeyboardButton(text='Увімкнути сповіщення')]],
                           resize_keyboard=True,
                           input_field_placeholder='Виберіть вже щось...',)
