# -*- coding: utf-8 -*-
"""
Готовий код Telegram-бота з використанням вебхука.
Цей скрипт призначений для розгортання на серверах, таких як Render.
"""

import telebot
import random
import os
from flask import Flask, request

# Вставте свій API-токен, який ви отримали від @BotFather
# Рекомендовано зберігати токен у змінних оточення для безпеки.
# У Render це можна зробити на вкладці "Environment".
API_TOKEN = os.environ.get('API_TOKEN')

# URL-адреса картинки для привітання.
WELCOME_IMAGE_URL = 'https://i.postimg.cc/9M6sr63K/angel-elohim-sacral-harmony-ohm2kwvmogb3vf6c416z-3.png?text=Вітаю+світла+душа'

# Список ваших підказок.
# Ви можете замінити цей список на повні 600 варіантів.
TIPS = [
    "Дива трапляються навколо тебе. Просто навчися їх помічати.",
    "Незалежно від того, наскільки далекою здається мета, йди до неї.",
    "Потрібно поговорити з людиною, з якою, як ти вважаєш, втратив зв'язок.",
    "Створи щось сьогодні. Будь то малюнок, вірш або просто нова ідея.",
    "Спробуй щось нове і вийди за межі своєї зони комфорту.",
    "Не забувай робити паузи, щоб насолодитися красою моменту."
]

# Створення екземпляра бота.
bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

# Обробник для команди /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Ця функція надсилає вітальне повідомлення та клавіатуру.
    """
    # Створення кнопки
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Отримати підказку'))

    # Текст привітання
    welcome_text = "Вітаю, світла душа! Я твій провідник у світі гармонії та інтуїції. Зазирни у себе, натиснувши кнопку нижче, і отримай підказку, що допоможе тобі відчути цей момент."

    # Надсилання вітального повідомлення з фото та клавіатурою
    bot.send_photo(
        message.chat.id,
        photo=WELCOME_IMAGE_URL,
        caption=welcome_text,
        reply_markup=keyboard
    )

# Обробник для тексту "Отримати підказку"
@bot.message_handler(func=lambda message: message.text == 'Отримати підказку')
def send_daily_tip(message):
    """
    Ця функція викликається, коли користувач натискає кнопку.
    Вона обирає випадкову підказку зі списку TIPS і надсилає її.
    """
    # Випадковий вибір підказки
    tip = random.choice(TIPS)

    # Надсилання підказки користувачеві
    bot.send_message(
        message.chat.id,
        tip,
        reply_markup=telebot.types.ReplyKeyboardRemove() # Приховуємо клавіатуру після надсилання підказки
    )

    # Додатково можна надіслати повідомлення, що бот чекає на наступний запит
    bot.send_message(message.chat.id, "Хочете отримати ще одну підказку? Просто напишіть /start")


# Цей блок налаштовує вебхук для роботи на Render
@server.route('/' + API_TOKEN, methods=['POST'])
def get_message():
    """Отримує оновлення від Telegram і обробляє їх."""
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route('/')
def webhook():
    """Встановлює вебхук для бота, коли сервер запускається."""
    # URL вебхука, який Render надає вашому сервісу.
    # Встановіть змінну оточення WEBHOOK_URL в налаштуваннях Render.
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get('WEBHOOK_URL') + '/' + API_TOKEN)
    return "WebHook встановлено!", 200

# Запуск сервера
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

