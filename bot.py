import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# ================= НАСТРОЙКИ =================
BOT_TOKEN = "7989675191:AAFnkhfIaZRrDh4LBIpYyZkoYTQOmzgrRso"
ADMIN_ID = 7621656595  # <-- ВСТАВЬ СВОЙ TELEGRAM ID (цифры)
ADMIN_USERNAME = "@Ibracc7"

# ================= ТЕКСТЫ =================
START_TEXT = (
    "🍎 *Сертификат разработчика iOS*\n"
    "без ПК • без jailbreak • за 5 минут\n\n"
    "✅ Установка IPA на iPhone\n"
    "✅ Работает на iOS 16–26\n"
    "✅ Подходит для Scarlet / AltStore\n"
    "✅ Единоразовая оплата\n\n"
    "👇 Нажмите кнопку ниже, чтобы продолжить"
)

CHOOSE_CERT_TEXT = (
    "📦 *Выберите сертификат*\n\n"
    "🔹 *Обычный — 250₽*\n"
    "Подходит для теста\n\n"
    "🔹 *Super обычный — 350₽* ⭐️\n"
    "Лучший выбор по стабильности\n\n"
    "🍎 *Мгновенный — 500₽*\n"
    "Выдача без ожидания\n\n"
    "⚡ *Super мгновенный — 700₽*\n"
    "Максимальная стабильность\n\n"
    "🍎 *Ultra мгновенный — 2000₽*\n"
    "Для постоянного использования"
)

CARD_TEXT = (
    "🔐 *Безопасная оплата*\n\n"
    "• Проверка вручную\n"
    "• Поддержка до результата\n\n"
    "💳 *Реквизиты:*\n\n"
    "💰 Карта: `2200 1545 3850 3250`\n"
    "🏦 СБП: Альфа-Банк\n"
    "📱 Телефон: `+7 993 777-71-28`\n\n"
    "📸 После оплаты нажмите *«💳 Я оплатил»* "
    "и отправьте скриншот"
)

WAIT_SCREENSHOT_TEXT = (
    "✅ *Отлично!*\n\n"
    "📸 Отправьте *скриншот оплаты*\n"
    "⏱ Проверка занимает 1–5 минут"
)

UDID_INSTRUCTION = (
    "💳 *Оплата подтверждена!* ✅\n\n"
    "📱 *Теперь отправьте UDID*\n\n"
    "1️⃣ Перейдите 👉 https://udid.tech\n"
    "2️⃣ Нажмите *Get UDID*\n"
    "3️⃣ Разрешите установку профиля\n"
    "4️⃣ Скопируйте UDID и отправьте сюда\n\n"
    "🎥 Видео-инструкция:\n"
    "https://youtube.com/shorts/xQ_xSXjtm-4\n\n"
    "⚠️ Отправляйте *ТОЛЬКО UDID*"
)

CERT_READY_TEXT = (
    "🎉 *Сертификат готов!* 🍎\n\n"
    "Теперь вы можете:\n"
    "• Устанавливать IPA\n"
    "• Использовать Scarlet / AltStore\n\n"
    "📥 Инструкция по установке будет отправлена далее\n\n"
    "💬 Поддержка: "
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

# ================= СТАРТ =================
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(START_TEXT, reply_markup=main_menu())

@dp.message(lambda m: m.text == "🛒 Купить сертификат")
async def choose_cert(message: types.Message):
    await message.answer(CHOOSE_CERT_TEXT, reply_markup=cert_menu())

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
    await message.answer(WAIT_SCREENSHOT_TEXT)

# ================= СКРИН =================
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
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="✅ Подтвердить оплату",
                callback_data=f"confirm_{user.id}"
            )]
        ])
    )

    await message.answer("✅ Скрин получен, ожидайте подтверждение")

# ================= ПОДТВЕРЖДЕНИЕ =================
@dp.callback_query(lambda c: c.data.startswith("confirm_"))
async def confirm_payment(callback: types.CallbackQuery):
    try:
        user_id = int(callback.data.split("_")[1])
        await callback.answer("✅ Оплата подтверждена")

        await bot.send_message(user_id, UDID_INSTRUCTION)
        await bot.send_message(ADMIN_ID, f"✅ Оплата подтверждена для пользователя ID: {user_id}")

    except Exception as e:
        await callback.answer(f"❌ Ошибка: {e}")

# ================= UDID =================
@dp.message(lambda m: m.text and len(m.text) > 20 and " " not in m.text)
async def receive_udid(message: types.Message):
    user = message.from_user

    await bot.send_message(
        ADMIN_ID,
        f"📱 *UDID ПОЛУЧЕН*\n\n"
        f"👤 @{user.username or 'без username'}\n"
        f"🆔 {user.id}\n"
        f"📛 {user.full_name}\n\n"
        f"`{message.text}`",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="📦 Сертификат выдан",
                callback_data=f"cert_{user.id}"
            )]
        ])
    )

    await message.answer("✅ UDID принят, выпускаем сертификат")

# ================= ВЫДАЧА =================
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
