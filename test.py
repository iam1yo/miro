import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from telegram.request import HTTPXRequest

# ==========================
# НАСТРОЙКИ
# ==========================

import os

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
MIRO_TOKEN = os.getenv("MIRO_TOKEN")
BOARD_ID = os.getenv("BOARD_ID")

# Только этот Telegram ID имеет доступ
MY_TELEGRAM_ID = 1051471957


# ==========================
# ДОБАВЛЕНИЕ ЗАМЕТКИ В MIRO
# ==========================

def add_note(text):
    url = f"https://api.miro.com/v2/boards/uXjVH74Yyjc=/sticky_notes"

    headers = {
        "Authorization": f"Bearer {MIRO_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "data": {
            "content": text
        },
        "position": {
            "x": 0,
            "y": 0
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    print(response.status_code, response.text)


# ==========================
# ОБРАБОТКА СООБЩЕНИЙ
# ==========================

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Проверка пользователя
    if update.effective_user.id != MY_TELEGRAM_ID:
        await update.message.reply_text("⛔ У вас нет доступа к этому боту.")
        return

    text = update.message.text

    add_note(text)

    await update.message.reply_text("✅ Добавил на Miro")


# ==========================
# ЗАПУСК БОТА
# ==========================

request = HTTPXRequest(
    connect_timeout=120,
    read_timeout=120,
    write_timeout=120
)

app = (
    Application.builder()
    .token(TELEGRAM_TOKEN)
    .request(request)
    .build()
)

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, message)
)

print("Бот работает...")

app.run_polling(poll_interval=3)