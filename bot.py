import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)

TOKEN = "7989675191:AAFnkhfIaZRrDh4LBIpYyZkoYTQOmzgrRso"

ADMIN_USERNAME = "@Ibracc7"

# ===== КНОПКИ =====

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🛒 Купить сертификат")]],
    resize_keyboard=True
)

certs_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔹 Обычный — 250₽")],
        [KeyboardButton(text="🔹 Super обычный — 350₽")],
        [KeyboardButton(text="🍎 Мгновенный — 500₽")],
        [KeyboardButton(text="⚡ Super мгновенный — 700₽")],
        [KeyboardButton(text="🍎 Ultra мгновенный — 2000₽")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)

confirm_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💳 Я оплатил")],
        [KeyboardButton(text="🔙 Назад к выбору")]
    ],
    resize_keyboard=True
)

# ===== БОТ =====

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(message: Message):
        await message.answer(
            "👋 Добро пожаловать!\n\n"
            "Здесь вы можете купить сертификат разработчика для iPhone 🍎",
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
            f"✅ Вы выбрали:\n\n{message.text}\n\n"
            "💳 *Оплата вручную*\n\n"
            "Переведите сумму удобным способом:\n"
            "━━━━━━━━━━━━━━\n"
            "💳 *Карта:* `2200 1545 3850 3250`\n"
            "🏦 *СБП:* Альфа-Банк\n"
            "📱 `+7 993 777 71 28`\n"
            "━━━━━━━━━━━━━━\n\n"
            "После оплаты нажмите кнопку **«Я оплатил»** и отправьте скрин.",
            reply_markup=confirm_keyboard,
            parse_mode="Markdown"
        )

    @dp.message(lambda m: m.text == "🔙 Назад к выбору")
    async def back(message: Message):
        await message.answer(
            "📦 Выберите сертификат 👇",
            reply_markup=certs_keyboard
        )

    @dp.message(lambda m: m.text == "💳 Я оплатил")
    async def paid(message: Message):
        await message.answer(
            "📸 Пожалуйста, отправьте скриншот оплаты одним сообщением.\n\n"
            "После проверки мы выдадим сертификат."
        )

    @dp.message(lambda m: m.photo)
    async def get_check(message: Message):
        await message.answer(
            "✅ Спасибо! Оплата получена и отправлена на проверку.\n"
            "Мы свяжемся с вами в ближайшее время."
        )

        await bot.send_message(
            ADMIN_USERNAME,
            f"💰 *НОВАЯ ОПЛАТА*\n\n"
            f"👤 Пользователь: @{message.from_user.username}\n"
            f"🆔 ID: {message.from_user.id}\n\n"
            f"Проверь скрин и выдай сертификат.",
            parse_mode="Markdown"
        )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
