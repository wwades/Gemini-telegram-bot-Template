import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import Command
from dotenv import load_dotenv
import google.generativeai as genai

# Загружаем ключи
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN or not GEMINI_KEY:
    print("Ошибка: Ключи не найдены в переменных окружения!")


session = AiohttpSession()

#  Настройка Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

#  Инициализация бота
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Спрашивай что угодно.")


@dp.message()
async def handle_message(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        # Запрос к нейросети
        response = model.generate_content(message.text)

        # Отправка ответа
        if response.text:
            await message.reply(response.text)
        else:
            await message.reply("Gemini прислал пустой ответ.")

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer(
            "Произошла ошибка доступа. Попробуй включить VPN на компьютере и перезапустить бота."
        )


async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
