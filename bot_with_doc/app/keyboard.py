from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton)
import app.database.requests as db

reg = [
    [KeyboardButton(text='Зарегистрироваться')]
]
reg_kb = ReplyKeyboardMarkup(keyboard=reg,
                             resize_keyboard=True)
change_email = [
    [KeyboardButton(text='Поменять email')]
]
change_email_kb = ReplyKeyboardMarkup(keyboard=change_email,
                                      resize_keyboard=True)

main = [
    [KeyboardButton(text='Документация')],
    [KeyboardButton(text='Мой токен')]
]
main_kb = ReplyKeyboardMarkup(keyboard=main,
                              resize_keyboard=True)
api_doc = [
    [KeyboardButton(text='Рассылка на email')],
    [KeyboardButton(text='Проверка email')],
    [KeyboardButton(text='Главное меню')]
]
api_doc_kb = ReplyKeyboardMarkup(keyboard=api_doc,
                                 resize_keyboard=True)
resume = [
    [KeyboardButton(text='Далее')]
]
resume_kb = ReplyKeyboardMarkup(keyboard=resume,
                                resize_keyboard=True)