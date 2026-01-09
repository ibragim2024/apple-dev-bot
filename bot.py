import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7989675191:AAFnkhfIaZRrDh4LBIpYyZkoYTQOmzgrRso"

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Главное меню
    main_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 Купить сертификат")],
        ],
        resize_keyboard=True
    )

    # Кнопки для выбора сертификатов
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

    # Обработчик команды /start
    @dp.message(CommandStart())
    async def start(message: Message):
        await message.answer(
            "👋 Добро пожаловать!\n\n"
            "Я помогу купить сертификат разработчика для iPhone 🍎\n\n"
            "Нажмите кнопку ниже 👇",
            reply_markup=main_keyboard
        )

    # Показ сертификатов
    @dp.message(lambda msg: msg.text == "🛒 Купить сертификат")
    async def show_certs(message: Message):
        await message.answer(
            "📦 Доступные сертификаты:\n\n"
            "Выберите подходящий сертификат ниже 👇",
            reply_markup=certs_keyboard
        )

    # Обработка выбора сертификата
    @dp.message(lambda msg: msg.text in [
        "🔹 Обычный — 250₽",
        "🔹 Super обычный — 350₽",
        "🍎 Мгновенный — 500₽",
        "⚡ Super мгновенный — 700₽",
        "🍎 Ultra мгновенный — 2000₽"
    ])
    async def choose_cert(message: Message):
        if message.text == "🔹 Обычный — 250₽":
            response = "✅ Вы выбрали:\n\n🔹 Обычный — 250₽\n❌ Без гарантии"
        elif message.text == "🔹 Super обычный — 350₽":
            response = "✅ Вы выбрали:\n\n🔹 Super обычный — 350₽\n✅ Гарантия 1 месяц"
        elif message.text == "🍎 Мгновенный — 500₽":
            response = "✅ Вы выбрали:\n\n🍎 Мгновенный — 500₽\n❌ Без гарантии"
        elif message.text == "⚡ Super мгновенный — 700₽":
            response = "✅ Вы выбрали:\n\n⚡ Super мгновенный — 700₽\n✅ Гарантия 1 месяц"
        elif message.text == "🍎 Ultra мгновенный — 2000₽":
            response = "✅ Вы выбрали:\n\n🍎 Ultra мгновенный — 2000₽\n✅ Гарантия 1 ГОД"

        # Кнопки для подтверждения выбора
        confirmation_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✅ Продолжить оплату")],
                [KeyboardButton(text="🔙 Назад к выбору")]
            ],
            resize_keyboard=True
        )

        await message.answer(response + "\n\n👉 Подтвердите действие:", reply_markup=confirmation_keyboard)

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
