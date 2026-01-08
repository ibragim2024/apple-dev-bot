from aiogram import Bot, Dispatcher, executor, types
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer(
        "👋 Добро пожаловать!\n\n"
        "Магазин Apple Developer Services\n\n"
        "Напиши /certs чтобы выбрать сертификат"
    )

@dp.message_handler(commands=["certs"])
async def certs(msg: types.Message):
    await msg.answer(
        "📱 Сертификаты:\n\n"
        "🔹 Обычный — 250₽\n"
        "🔹 Super обычный — 350₽\n"
        "🍎 Мгновенный — 500₽\n"
        "⚡ Super мгновенный — 700₽\n"
        "🍎 Ultra мгновенный — 2000₽"
    )

if __name__ == "__main__":
    executor.start_polling(dp)
