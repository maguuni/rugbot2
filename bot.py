import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет! Пришли фото ковра — сделаю карточку товара 👌")

@dp.message()
async def handle_photo(message: types.Message):
    if not message.photo:
        await message.answer("Пришли именно фото 📸")
        return

    await message.answer("Фото получил. Генерирую карточку товара…")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": "Сделай продающее описание ковра для маркетплейса"
            }
        ]
    }

    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    text = r.json()["choices"][0]["message"]["content"]
    await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
