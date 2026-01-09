import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

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
    @dp.message(CommandStart())
    async def start(message: Message):
        await message.answer(
            "👋 Добро пожаловать!\n\n"
            "Здесь вы можете приобрести сертификат разработчика для iPhone.\n\n"
            "Выберите действие 👇",
            reply_markup=keyboard
        )

    # Кнопка "Купить сертификат"
    @dp.message(F.text.in_(["1", "2", "3", "4", "5"]))
async def choose_cert(message: Message):
    choices = {
        "1": "🔹 Обычный — 250₽ (3 дня)\n❌ Без гарантии",
        "2": "🔹 Super обычный — 350₽ (3 дня)\n✅ Гарантия 1 месяц",
        "3": "🍎 Мгновенный — 500₽ (10 мин)\n❌ Без гарантии",
        "4": "⚡ Super мгновенный — 700₽ (10 мин)\n✅ Гарантия 1 месяц",
        "5": "🍎 Ultra — 2000₽ (10 мин)\n✅ Гарантия 1 ГОД"
    }

    await message.answer(
        f"✅ Вы выбрали:\n\n{choices[message.text]}\n\n"
        "Напишите `да` для подтверждения или `нет` для отмены."
    )
    # Обрабатываем цифры 1–5
    @dp.message(F.text.in_(["1", "2", "3", "4", "5"]))
    async def choose_certificate(message: Message):
        choice = message.text
        if choice == "1":
            response = "✅ Вы выбрали сертификат:\n\n🔹 Обычный — 250₽ (3 дня)\n❌ без гарантии"
            price = 250
        elif choice == "2":
            response = "✅ Вы выбрали сертификат:\n\n🔹 Super обычный — 350₽ (3 дня)\n✅ гарантия 1 месяц"
            price = 350
        elif choice == "3":
            response = "✅ Вы выбрали сертификат:\n\n🍎 Мгновенный — 500₽ (10 мин)\n❌ без гарантии"
            price = 500
        elif choice == "4":
            response = "✅ Вы выбрали сертификат:\n\n⚡ Super мгновенный — 700₽ (10 мин)\n✅ гарантия 1 месяц"
            price = 700
        elif choice == "5":
            response = "✅ Вы выбрали сертификат:\n\n🍎 Ultra мгновенный — 2000₽ (10 мин)\n✅ гарантия 1 ГОД"
            price = 2000

        # Генерация ссылки для оплаты
        payment_url = create_payment(price, response)
        
        # Подтверждение с кнопками
        confirmation_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✅ Продолжить оплату")],
                [KeyboardButton(text="🔙 Назад к выбору")]
            ],
            resize_keyboard=True
        )

        await message.answer(response + f"\n\n👉 Перейдите по ссылке для оплаты: {payment_url}", reply_markup=confirmation_keyboard)

    # Кнопка "Назад"
    @dp.message(lambda message: message.text == "🔙 Назад к выбору")
    async def back_to_choice(message: Message):
        await message.answer(
            "📦 *Доступные сертификаты:*\n\n"
            "🔹 1. Обычный — 250₽ (3 дня)\n❌ без гарантии\n\n"
            "🔹 2. Super обычный — 350₽ (3 дня)\n✅ гарантия 1 месяц\n\n"
            "🍎 3. Мгновенный — 500₽ (10 мин)\n❌ без гарантии\n\n"
            "⚡ 4. Super мгновенный — 700₽ (10 мин)\n✅ гарантия 1 месяц\n\n"
            "🍎 5. Ultra мгновенный — 2000₽ (10 мин)\n✅ гарантия 1 ГОД\n\n"
            "👉 Напишите номер варианта (1–5)",
            parse_mode="Markdown"
        )

    # Кнопка "Продолжить оплату"
    @dp.message(lambda message: message.text == "✅ Продолжить оплату")
    async def continue_payment(message: Message):
        await message.answer(
            "💳 Для завершения покупки — выберите способ оплаты."
        )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
