import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
import uuid

# ================= НАСТРОЙКИ =================
BOT_TOKEN = "7989675191:AAFnkhfIaZRrDh4LBIpYyZkoYTQOmzgrRso"

ADMIN_ID = 7621656595  # <-- ТВОЙ TELEGRAM ID
ADMIN_USERNAME = "@Ibracc7"

CARD_TEXT = (
    "💳 *Оплата вручную*\n\n"
    "💰 *Карта:* `2200 1545 3850 3250`\n"
    "🏦 *СБП:* Альфа-Банк\n"
    "📱 *Телефон:* `+7 993 777-71-28`\n\n"
    "📸 После оплаты нажмите «💳 Я оплатил» и отправьте скриншот"
)

UDID_INSTRUCTION = (
    "📱 *Отправьте ваш UDID*\n\n"
    "🔹 *Способ 1 (самый простой):*\n"
    "1️⃣ Перейдите на сайт 👉 https://udid.tech\n"
    "2️⃣ Нажмите *Get UDID*\n"
    "3️⃣ Разрешите установку профиля\n"
    "4️⃣ Скопируйте UDID и отправьте сюда\n\n"
    "🎥 *Видео-инструкция:*\n"
    "https://youtu.be/9zE0s9GJ7bA\n\n"
    "⚠️ Отправляйте *ТОЛЬКО UDID* (буквы и цифры)"
)

bot = Bot(token=BOT_TOKEN, parse_mode="Markdown")
dp = Dispatcher()

# ================= КНОПКИ =================
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🛒 Купить сертификат")]],
        resize_keyboard=True
    )

def cert_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔹 Обычный — 250₽")],
            [KeyboardButton(text="🔹 Super обычный — 350₽")],
            [KeyboardButton(text="🍎 Мгновенный — 500₽")],
            [KeyboardButton(text="⚡ Super мгновенный — 700₽")],
            [KeyboardButton(text="🍎 Ultra мгновенный — 2000₽")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )

def pay_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💳 Я оплатил")],
            [KeyboardButton(text="⬅️ Назад к выбору")]
        ],
        resize_keyboard=True
    )

# ================= ХЕНДЛЕРЫ =================
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 *Добро пожаловать!*\n\n"
        "Здесь вы можете купить *сертификат разработчика iPhone* 🍎",
        reply_markup=main_menu()
    )

@dp.message(lambda m: m.text == "🛒 Купить сертификат")
async def choose_cert(message: types.Message):
    await message.answer("📦 *Выберите сертификат:*", reply_markup=cert_menu())

@dp.message(lambda m: m.text in [
    "🔹 Обычный — 250₽",
    "🔹 Super обычный — 350₽",
    "🍎 Мгновенный — 500₽",
    "⚡ Super мгновенный — 700₽",
    "🍎 Ultra мгновенный — 2000₽"
])
async def payment_info(message: types.Message):
    await message.answer(CARD_TEXT, reply_markup=pay_menu())

@dp.message(lambda m: m.text == "💳 Я оплатил")
async def wait_screenshot(message: types.Message):
    await message.answer(
        "📸 *Отправьте скриншот оплаты*\n\n"
        "⚠️ Принимаются только изображения."
    )

# ================= ПРИЁМ СКРИНА =================
@dp.message(lambda m: m.photo)
async def receive_screenshot(message: types.Message):
    user = message.from_user
    photo_id = message.photo[-1].file_id
    payment_id = uuid.uuid4()

    caption = (
        "💰 *НОВАЯ ОПЛАТА*\n\n"
        f"👤 @{user.username or 'без username'}\n"
        f"🆔 ID: {user.id}\n"
        f"📛 Имя: {user.full_name}"
    )

    await bot.send_photo(
        ADMIN_ID,
        photo_id,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить",
                    callback_data=f"confirm_{user.id}"
                )
            ]
        ])
    )

    await message.answer(
        "✅ *Скриншот получен!*\n\n"
        "После проверки вам нужно будет отправить UDID."
    )

# ================= ПОДТВЕРЖДЕНИЕ =================
@dp.callback_query(lambda c: c.data.startswith("confirm_"))
async def confirm_payment(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[1])

    await bot.send_message(user_id, UDID_INSTRUCTION)
    await callback.answer("Оплата подтверждена")

# ================= ПРИЁМ UDID =================
@dp.message(lambda m: m.text and len(m.text) > 20 and " " not in m.text)
async def receive_udid(message: types.Message):
    user = message.from_user
    udid = message.text.strip()

    await bot.send_message(
        ADMIN_ID,
        "📱 *UDID ПОЛУЧЕН*\n\n"
        f"👤 @{user.username or 'без username'}\n"
        f"🆔 ID: {user.id}\n"
        f"📛 Имя: {user.full_name}\n\n"
        f"`{udid}`"
    )

    await message.answer(
        "✅ *UDID получен!*\n\n"
        "Мы начали выпуск сертификата.\n"
        "Ожидайте сообщение от администратора 👌"
    )

@dp.message(lambda m: m.text in ["⬅️ Назад", "⬅️ Назад к выбору"])
async def back(message: types.Message):
    await message.answer("📦 *Выберите сертификат:*", reply_markup=cert_menu())

# ================= ЗАПУСК =================
async def main():
    print("Бот запущен и работает")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
