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

    # /start
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
            "1️⃣ Обычный — 250₽ (3 дня)\n❌ без гарантии\n\n"
            "2️⃣ Super обычный — 350₽ (3 дня)\n✅ гарантия 1 месяц\n\n"
            "3️⃣ 🍎 Мгновенный — 500₽ (10 мин)\n❌ без гарантии\n\n"
            "4️⃣ ⚡ Super мгновенный — 700₽ (10 мин)\n✅ гарантия 1 месяц\n\n"
            "5️⃣ 🍎 Ultra мгновенный — 2000₽ (10 мин)\n✅ гарантия 1 ГОД\n\n"
            "👉 Напишите цифру от 1 до 5"
        )

    # Обработка цифр
    @dp.message(lambda msg: msg.text in ["1", "2", "3", "4", "5"])
    async def choose_cert(message: Message):
        answers = {
            "1": "🔹 Обычный — 250₽\n⏳ 3 дня\n❌ Без гарантии",
            "2": "🔹 Super обычный — 350₽\n⏳ 3 дня\n✅ Гарантия 1 месяц",
            "3": "🍎 Мгновенный — 500₽\n⚡ 10 минут\n❌ Без гарантии",
            "4": "⚡ Super мгновенный — 700₽\n⚡ 10 минут\n✅ Гарантия 1 месяц",
            "5": "🍎 Ultra мгновенный — 2000₽\n⚡ 10 минут\n✅ Гарантия 1 ГОД",
        }

        await message.answer(
            f"✅ Вы выбрали:\n\n{answers[message.text]}\n\n"
            "На следующем шаге добавим оплату 💳"
        )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
