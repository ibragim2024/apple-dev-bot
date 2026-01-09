import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 Купить сертификат")],
            [KeyboardButton(text="ℹ️ Информация")]
        ],
        resize_keyboard=True
    )

    @dp.message(CommandStart())
    async def start(message: Message):
        await message.answer(
            "👋 Добро пожаловать!\n\n"
            "Здесь вы можете приобрести сертификат разработчика для iPhone.\n\n"
            "Выберите действие 👇",
            reply_markup=keyboard
        )

    @dp.message(lambda m: m.text == "🛒 Купить сертификат")
    async def buy(message: Message):
        await message.answer(
            "📦 *Доступные сертификаты:*\n\n"
            "🔹 Обычный — 250₽ (3 дня)\n❌ без гарантии\n\n"
            "🔹 Super обычный — 350₽ (3 дня)\n✅ гарантия 1 месяц\n\n"
            "🍎 Мгновенный — 500₽ (10 мин)\n❌ без гарантии\n\n"
            "⚡ Super мгновенный — 700₽ (10 мин)\n✅ гарантия 1 месяц\n\n"
            "🍎 Ultra мгновенный — 2000₽ (10 мин)\n✅ гарантия 1 ГОД\n\n"
            "👉 Напишите номер варианта (1–5)",
            parse_mode="Markdown"
        )

    @dp.message(lambda m: m.text == "ℹ️ Информация")
    async def info(message: Message):
        await message.answer(
            "📄 После оплаты вы получите сертификат и инструкцию.\n"
            "⏱ Сроки зависят от выбранного тарифа.\n"
            "💬 Поддержка работает 24/7."
        )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
