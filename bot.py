import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from payments import create_payment  # импортируем функцию создания платежа

TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Основное меню
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 Купить сертификат")],
            [KeyboardButton(text="ℹ️ Информация")]
        ],
        resize_keyboard=True
    )

    # При старте бота
@dp.message(F.text.in_(["1", "2", "3", "4", "5"]))
async def choose_certificate(message: Message):
    choice = message.text

    if choice == "1":
        text = (
            "✅ Вы выбрали сертификат:\n\n"
            "🔹 Обычный — 250₽\n"
            "⏳ Срок: до 3 дней\n"
            "❌ Гарантия: отсутствует"
        )
        price = 250

    elif choice == "2":
        text = (
            "✅ Вы выбрали сертификат:\n\n"
            "🔹 Super обычный — 350₽\n"
            "⏳ Срок: до 3 дней\n"
            "✅ Гарантия: 1 месяц"
        )
        price = 350

    elif choice == "3":
        text = (
            "✅ Вы выбрали сертификат:\n\n"
            "🍎 Мгновенный — 500₽\n"
            "⏱ Срок: 10 минут\n"
            "❌ Гарантия: отсутствует"
        )
        price = 500

    elif choice == "4":
        text = (
            "✅ Вы выбрали сертификат:\n\n"
            "⚡ Super мгновенный — 700₽\n"
            "⏱ Срок: 10 минут\n"
            "✅ Гарантия: 1 месяц"
        )
        price = 700

    elif choice == "5":
        text = (
            "✅ Вы выбрали сертификат:\n\n"
            "🍎 Ultra мгновенный — 2000₽\n"
            "⏱ Срок: 10 минут\n"
            "✅ Гарантия: 1 ГОД"
        )
        price = 2000

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Продолжить оплату")],
            [KeyboardButton(text="🔙 Назад к выбору")]
        ],
        resize_keyboard=True
    )

    await message.answer(text + "\n\n👉 Подтвердите действие:", reply_markup=keyboard)
