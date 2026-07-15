import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters


TELEGRAM_TOKEN = "8669146655:AAG4qkWbxJagM-c9ArBAJUvCn5ccnbon8Og"

MIRO_TOKEN = "eyJtaXJvLm9yaWdpbiI6ImV1MDEifQ_Ezkh9hNMNgqHuCfqsTUjOFL5iL0"

BOARD_ID = "uXjVH74Yyjc="


def add_note(text):
    url = f"https://api.miro.com/v2/boards/{BOARD_ID}/sticky_notes"

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


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    add_note(text)

    await update.message.reply_text(
        "✅ Добавил на Miro"
    )


from telegram.request import HTTPXRequest

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
    MessageHandler(filters.TEXT, message)
)

print("Бот работает")

from telegram.request import HTTPXRequest

request = HTTPXRequest(
    connect_timeout=120,
    read_timeout=120,
    write_timeout=120
)

app.run_polling(
    poll_interval=3
)

app.run_polling(
    poll_interval=3
)