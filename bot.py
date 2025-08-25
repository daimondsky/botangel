# -*- coding: utf-8 -*-
"""Готовий код Telegram-бота з вебхуком

Цей код створює невеликий вебсервер за допомогою Flask
і налаштовує вебхук для отримання повідомлень від Telegram.
"""

import telebot
import random
import time
import os
from flask import Flask, request

# Вставте свій API-токен, який ви отримали від @BotFather.
# Ми будемо брати його з змінних оточення Render.
API_TOKEN = os.environ.get('API_TOKEN')

if not API_TOKEN:
    print("Помилка: Не знайдено змінну оточення API_TOKEN.")
    exit()

# URL-адреса картинки для привітання.
# Замініть це посилання на власне зображення.
WELCOME_IMAGE_URL = 'https://i.postimg.cc/9M6sr63K/angel-elohim-sacral-harmony-ohm2kwvmogb3vf6c416z-3.png?text=Вітаю+світла+душа'

# Список ваших підказок.
# Замініть цей список на повні 600 варіантів.
TIPS = [
    "Дива трапляються навколо тебе. Просто навчися їх помічати.",
    "Незалежно від того, наскільки далекою здається мета, йди до неї.",
    "Потрібно поговорити з людиною, з якою, як ти вважаєш, розмова не складеться. Це відкриє нові двері.",
    "Твоя сила — це твоя унікальність. Прийми її, а не ховай.",
    "Щоб змінити світ, почни зі зміни свого ставлення до нього.",
    "Довіряй своїй інтуїції, вона завжди знає дорогу.",
    "Будь вдячним за те, що маєш, і це примножиться.",
    "Світ чекає на твою усмішку.",
    "Кожен крок, навіть найменший, веде до твоєї мети."
]

# Ініціалізація бота та Flask-додатка
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Обробник для команди /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Ця функція надсилає привітання та клавіатуру.
    """
    # Створення клавіатури з кнопкою "Отримати підказку"
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
    button_tip = telebot.types.KeyboardButton('Отримати підказку')
    keyboard.add(button_tip)

    # Текст привітання
    welcome_text = "Привіт, світла душе! ✨\n\nЯ тут, щоб допомогти тобі щодня знаходити натхнення та позитив. Якщо тобі потрібна мудра порада або просто підказка, натисни кнопку нижче."

    # Надсилання картинки та привітального тексту з клавіатурою
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
        # Ми не приховуємо клавіатуру, щоб користувач міг натиснути кнопку знову
    )

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Код нижче налаштовує вебхук для роботи на вебсервісі, такому як Render. #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Визначення URL вебхука
# Render надає URL у змінній оточення RENDER_EXTERNAL_HOSTNAME
WEBHOOK_HOST = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if not WEBHOOK_HOST:
    print("Помилка: Не знайдено змінну оточення RENDER_EXTERNAL_HOSTNAME.")
    exit()

WEBHOOK_URL_BASE = f"https://{WEBHOOK_HOST}"
WEBHOOK_URL_PATH = f"/{API_TOKEN}/"

# Основний маршрут для вебхука. Telegram надсилає сюди оновлення.
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    """
    Ця функція обробляє вхідні POST-запити від Telegram.
    """
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '!', 200
    else:
        return 'Wrong Content-Type', 403

# Маршрут для перевірки стану вебсервера
@app.route('/')
def index():
    """
    Простий маршрут для перевірки, чи працює сервер.
    """
    return 'Бот працює!', 200

def set_webhook_on_startup():
    """
    Встановлює вебхук під час запуску додатку.
    """
    print("Спроба встановити вебхук...")
    try:
        # Спершу видаляємо старий вебхук, якщо він існує
        bot.remove_webhook()
        time.sleep(1) # Затримка, щоб Telegram встиг обробити запит
        # Встановлюємо новий вебхук
        bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
        print("Вебхук встановлено успішно.")
    except Exception as e:
        print(f"Помилка при встановленні вебхука: {e}")

if __name__ == '__main__':
    # Встановлення вебхука та запуск сервера
    set_webhook_on_startup()
    # Запуск сервера Flask
    # host='0.0.0.0' потрібен для роботи на Render
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
