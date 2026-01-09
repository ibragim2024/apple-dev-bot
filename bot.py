import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# ================= НАСТРОЙКИ =================
BOT_TOKEN = "7989675191:AAFnkhfIaZRrDh4LBIpYyZkoYTQOmzgrRso"

ADMIN_ID = 7621656595  # ТВОЙ TELEGRAM ID
ADMIN_USERNAME = "@Ibracc7"

# ================= ТЕКСТЫ =================
CARD_TEXT = (
    "💳 Оплата вручную\n\n"
    "Карта: 2200 1545 3850 3250\n"
    "Банк: Альфа-Банк\n"
    "Телефон: +7 993 777-71-28\n\n"
    "После оплаты нажмите «Я оплатил» и отправьте скриншот"
)

UDID_INSTRUCTION = (
    "📱 Отправьте ваш UDID\n\n"
    "Как получить UDID:\n"
    "1. Перейдите на сайт: https://udid.tech\n"
    "2. Нажмите Get UDID\n"
    "3. Разрешите установку профиля\n"
    "4. Скопируйте UDID и отправьте его сюда\n\n"
    "Видео инструкция:\n"
    "https://youtube.com/shorts/xQ_xSXjtm-4\n\n"
    "Отправляйте ТОЛЬКО UDID"
)

CERT_READY_TEXT = (
    "🎉 Ваш сертификат разработчика готов!\n\n"
    "Теперь вы можете устанавливать приложения и подписывать IPA.\n\n"
    f"Если есть вопросы — {ADMIN_USERNAME}\n\n"
    "Спасибо за покупку ❤️"
)

# ================= БОТ =================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# ================= КНОПКИ =================
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🛒 Купить сертификат")]],
        resize_keyboard=True
    )

def cert_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Обычный — 250₽")],
            [KeyboardButton(text="Super обычный — 350₽")],
            [KeyboardButton(text="Мгновенный — 500₽")],
            [KeyboardButton(text="Super мгновенный — 700₽")],
            [KeyboardButton(text="Ultra мгновенный — 2000₽")],
        ],
        resize_keyboard=True
    )

def pay_menu():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="💳 Я оплатил")]],
        resize_keyboard=True
    )

# ================= ХЕНДЛЕРЫ =================
@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать!\n\nВы можете купить сертификат разработчика iPhone 🍎",
        reply_markup=main_menu()
    )

@router.message(lambda m: m.text == "🛒 Купить сертификат")
async def choose_cert(message: types.Message):
    await message.answer("Выберите сертификат:", reply_markup=cert_menu())

@router.message(lambda m: "₽" in (m.text or ""))
async def payment_info(message: types.Message):
    await message.answer(CARD_TEXT, reply_markup=pay_menu())

@router.message(lambda m: m.text == "💳 Я оплатил")
async def wait_screenshot(message: types.Message):
    await message.answer("Отправьте скриншот оплаты")

@router.message(lambda m: m.photo)
async def receive_screenshot(message: types.Message):
    user = message.from_user

    await bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=(
            f"НОВАЯ ОПЛАТА\n\n"
            f"User: @{user.username}\n"
            f"ID: {user.id}\n"
            f"Имя: {user.full_name}"
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="✅ Подтвердить оплату",
                callback_data=f"confirm_{user.id}"
            )]
        ])
    )

    await message.answer("Скрин получен, ожидайте подтверждение")

@router.callback_query(lambda c: c.data.startswith("confirm_"))
async def confirm_payment(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    await bot.send_message(user_id, UDID_INSTRUCTION)
    await callback.answer("Оплата подтверждена")

@router.message(lambda m: m.text and len(m.text) > 20 and " " not in m.text)
async def receive_udid(message: types.Message):
    user = message.from_user

    await bot.send_message(
        ADMIN_ID,
        f"UDID получен от @{user.username}\n\n{message.text}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="📦 Сертификат выдан",
                callback_data=f"cert_{user.id}"
            )]
        ])
    )

    await message.answer("UDID принят, выпускаем сертификат")

@router.callback_query(lambda c: c.data.startswith("cert_"))
async def certificate_ready(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    await bot.send_message(user_id, CERT_READY_TEXT)
    await callback.answer("Готово")

# ================= ЗАПУСК =================
async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
