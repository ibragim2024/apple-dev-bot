import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import uuid

# ================= НАСТРОЙКИ =================
BOT_TOKEN = "7989675191:AAFnkhfIaZRrDh4LBIpYyZkoYTQOmzgrRso"

ADMIN_ID = 7621656595  # <-- ВСТАВЬ СВОЙ TELEGRAM ID (цифры)
ADMIN_USERNAME = "@Ibracc7"

CARD_TEXT = (
    "💳 *Оплата вручную*\n\n"
    "💰 *Карта:* `2200 1545 3850 3250`\n"
    "🏦 *СБП:* Альфа-Банк\n"
    "📱 *Телефон:* `+7 993 777-71-28`\n\n"
    "📸 После оплаты нажмите «💳 Я оплатил» и отправьте скриншот"
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

# ====== ПРИЁМ СКРИНШОТА ======
@dp.message(lambda m: m.photo)
async def receive_screenshot(message: types.Message):
    user = message.from_user
    photo_id = message.photo[-1].file_id

    caption = (
        "💰 *СКРИНШОТ ОПЛАТЫ*\n\n"
        f"👤 Пользователь: @{user.username or 'без username'}\n"
        f"🆔 ID: {user.id}\n"
        f"📛 Имя: {user.full_name}"
    )

    # Сохраняем ID оплаты, чтобы админ мог подтвердить или отклонить
    payment_id = uuid.uuid4()

    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo_id,
        caption=caption,
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("✅ Подтвердить", callback_data=f"confirm_{payment_id}")
        ).add(
            InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{payment_id}")
        )
    )

    await message.answer(
        "✅ *Скриншот получен!*\n\n"
        "Администратор проверит оплату и свяжется с вами 👌"
    )

# ====== ОБРАБОТЧИКИ ДЛЯ ПОДТВЕРЖДЕНИЯ ОПЛАТЫ ======
@dp.callback_query(lambda c: c.data.startswith('confirm_'))
async def confirm_payment(callback_query: types.CallbackQuery):
    payment_id = callback_query.data.split('_')[1]
    await bot.answer_callback_query(callback_query.id)
    
    await bot.send_message(
        callback_query.from_user.id,
        f"✅ Оплата с ID {payment_id} подтверждена! Ожидайте получения сертификата."
    )

    await bot.send_message(
        ADMIN_ID,
        f"✅ Оплата с ID {payment_id} подтверждена."
    )

@dp.callback_query(lambda c: c.data.startswith('reject_'))
async def reject_payment(callback_query: types.CallbackQuery):
    payment_id = callback_query.data.split('_')[1]
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(
        callback_query.from_user.id,
        f"❌ Оплата с ID {payment_id} отклонена. Пожалуйста, проверьте реквизиты."
    )

    await bot.send_message(
        ADMIN_ID,
        f"❌ Оплата с ID {payment_id} отклонена."
    )

# ================= ЗАПУСК =================
async def main():
    print("Бот запущен и работает")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
