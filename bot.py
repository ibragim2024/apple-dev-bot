import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# ================= НАСТРОЙКИ =================
BOT_TOKEN = "7989675191:AAFnkhfIaZRrDh4LBIpYyZkoYTQOmzgrRso"
ADMIN_ID = 7621656595  # <-- ТВОЙ TELEGRAM ID
ADMIN_USERNAME = "@Ibracc7"

# ================= ТЕКСТЫ =================
START_TEXT = (
    "🍎 *Сертификат разработчика для iPhone*\n\n"
    "✅ Установка любых IPA\n"
    "✅ Без джейлбрейка\n"
    "✅ Работает на iOS 17–18\n"
    "⚡ От 10 минут\n\n"
    "👇 Выберите вариант ниже"
)

CERT_CHOOSE_TEXT = (
    "📦 *Выберите сертификат*\n\n"
    "⚠️ Если не знаете, какой выбрать —\n"
    "рекомендуем ⚡ *Super мгновенный*\n"
    "(лучший вариант по цене и гарантии)"
)

CARD_TEXT = (
    "💳 *Оплата вручную*\n\n"
    "💰 *Карта:* `2200 1545 3850 3250`\n"
    "🏦 *СБП:* Альфа-Банк\n"
    "📱 *Телефон:* `+7 993 777-71-28`\n\n"
    "ℹ️ *Как проходит покупка:*\n"
    "1️⃣ Вы оплачиваете\n"
    "2️⃣ Отправляете скрин\n"
    "3️⃣ Мы подтверждаем\n"
    "4️⃣ Вы отправляете UDID\n"
    "5️⃣ Получаете сертификат\n\n"
    "📸 После оплаты нажмите «💳 Я оплатил»"
)

UDID_INSTRUCTION = (
    "📱 *Отправьте ваш UDID*\n\n"
    "🔹 *Самый простой способ:*\n"
    "1️⃣ Перейдите 👉 https://udid.tech\n"
    "2️⃣ Нажмите *Get UDID*\n"
    "3️⃣ Разрешите профиль\n"
    "4️⃣ Скопируйте UDID и отправьте сюда\n\n"
    "🎥 Видео-инструкция:\n"
    "https://youtube.com/shorts/xQ_xSXjtm-4\n\n"
    "⚠️ Отправляйте *ТОЛЬКО UDID*"
)

CERT_READY_TEXT = (
    "🎉 *Ваш сертификат разработчика готов!*\n\n"
    "📌 Теперь вы можете:\n"
    "• Устанавливать приложения\n"
    "• Подписывать IPA\n"
    "• Использовать AltStore / Scarlet\n\n"
    "📩 По всем вопросам:\n"
    f"{ADMIN_USERNAME}\n\n"
    "Спасибо за покупку ❤️"
)

# ================= БОТ =================
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
            [KeyboardButton(text="⚡ Super мгновенный — 700₽ ⭐")],
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
    await message.answer(START_TEXT, reply_markup=main_menu())
    await asyncio.sleep(40)
    await message.answer(
        "💬 Если есть вопросы — всегда можно написать админу 👇\n"
        f"{ADMIN_USERNAME}"
    )

@dp.message(lambda m: m.text == "🛒 Купить сертификат")
async def choose_cert(message: types.Message):
    await message.answer(CERT_CHOOSE_TEXT, reply_markup=cert_menu())

@dp.message(lambda m: m.text == "⬅️ Назад")
async def back_main(message: types.Message):
    await message.answer(START_TEXT, reply_markup=main_menu())

@dp.message(lambda m: m.text == "⬅️ Назад к выбору")
async def back_cert(message: types.Message):
    await message.answer(CERT_CHOOSE_TEXT, reply_markup=cert_menu())

@dp.message(lambda m: m.text in [
    "🔹 Обычный — 250₽",
    "🔹 Super обычный — 350₽",
    "⚡ Super мгновенный — 700₽ ⭐",
    "🍎 Ultra мгновенный — 2000₽"
])
async def payment_info(message: types.Message):
    await message.answer(CARD_TEXT, reply_markup=pay_menu())

@dp.message(lambda m: m.text == "💳 Я оплатил")
async def wait_screenshot(message: types.Message):
    await message.answer("📸 *Отправьте скриншот оплаты*")

@dp.message(lambda m: m.photo)
async def receive_screenshot(message: types.Message):
    user = message.from_user

    await bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=(
            "💰 *НОВАЯ ОПЛАТА*\n\n"
            f"👤 @{user.username or 'без username'}\n"
            f"🆔 {user.id}\n"
            f"📛 {user.full_name}"
        ),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="✅ Подтвердить оплату",
                    callback_data=f"confirm_{user.id}"
                )]
            ]
        )
    )

    await message.answer("✅ Скрин получен, ожидайте подтверждение.")

@dp.callback_query(lambda c: c.data.startswith("confirm_"))
async def confirm_payment(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    await bot.send_message(user_id, UDID_INSTRUCTION)
    await callback.answer("Оплата подтверждена")

@dp.message(lambda m: m.text and len(m.text) > 20 and " " not in m.text)
async def receive_udid(message: types.Message):
    user = message.from_user

    await bot.send_message(
        ADMIN_ID,
        (
            "📱 *UDID ПОЛУЧЕН*\n\n"
            f"👤 @{user.username or 'без username'}\n"
            f"🆔 {user.id}\n"
            f"📛 {user.full_name}\n\n"
            f"`{message.text}`"
        ),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="📦 Сертификат выдан",
                    callback_data=f"cert_{user.id}"
                )]
            ]
        )
    )

    await message.answer("✅ UDID принят. Выпускаем сертификат.")

@dp.callback_query(lambda c: c.data.startswith("cert_"))
async def certificate_ready(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    await bot.send_message(user_id, CERT_READY_TEXT)
    await callback.answer("Готово")

# ================= ЗАПУСК =================
async def main():
    print("Бот запущен и работает")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
