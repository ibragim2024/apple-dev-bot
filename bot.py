import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7989675191:AAFnkhfIaZRrDh4LBIpYyZkoYTQOmzgrRso"

# ====== КЛАВИАТУРЫ ======

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛒 Купить сертификат")]
    ],
    resize_keyboard=True
)

certs_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔹 Обычный — 250₽")],
        [KeyboardButton(text="🔹 Super обычный — 350₽")],
        [KeyboardButton(text="🍎 Мгновенный — 500₽")],
        [KeyboardButton(text="⚡ Super мгновенный — 700₽")],
        [KeyboardButton(text="🍎 Ultra мгновенный — 2000₽")]
    ],
    resize_keyboard=True
)

confirm_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Продолжить оплату")],
        [KeyboardButton(text="🔙 Назад к выбору")]
    ],
    resize_keyboard=True
)

# ====== БОТ ======

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(message: Message):
        await message.answer(
            "👋 Добро пожаловать!\n\n"
            "Я помогу купить сертификат разработчика для iPhone 🍎",
            reply_markup=main_keyboard
        )

    @dp.message(lambda m: m.text == "🛒 Купить сертификат")
    async def show_certs(message: Message):
        await message.answer(
            "📦 Выберите сертификат 👇",
            reply_markup=certs_keyboard
        )

    @dp.message(lambda m: m.text in [
        "🔹 Обычный — 250₽",
        "🔹 Super обычный — 350₽",
        "🍎 Мгновенный — 500₽",
        "⚡ Super мгновенный — 700₽",
        "🍎 Ultra мгновенный — 2000₽"
    ])
    async def choose_cert(message: Message):
        await message.answer(
            f"✅ Вы выбрали:\n\n{message.text}\n\nПодтвердите действие 👇",
            reply_markup=confirm_keyboard
        )

    @dp.message(lambda m: m.text == "🔙 Назад к выбору")
    async def back(message: Message):
        await message.answer(
            "📦 Выберите сертификат 👇",
            reply_markup=certs_keyboard
        )

    @dp.message(lambda m: m.text == "✅ Продолжить оплату")
    async def pay(message: Message):
        await message.answer("💳 Оплата будет подключена на следующем шаге")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
