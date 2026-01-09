import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ====== НАСТРОЙКИ ======
BOT_TOKEN = "7989675191:AAFnkhfIaZRrDh4LBIpYyZkoYTQOmzgrRso"
ADMIN_ID = 7621656595  # ← сюда свой ID
ADMIN_USERNAME = "@Ibracc7"

# Реквизиты
CARD_TEXT = (
    "💳 *Оплата вручную*\n\n"
    "💰 *Карта:* `2200 1545 3850 3250`\n"
    "🏦 *СБП:* Альфа-Банк\n"
    "📱 *Телефон:* `+7 993 777-71-28`\n\n"
    "После оплаты нажмите кнопку «💳 Я оплатил»"
)

bot = Bot(token=BOT_TOKEN, parse_mode="Markdown")
dp = Dispatcher()

# ====== КНОПКИ ======
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 Купить сертификат")]
        ],
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

# ====== ХЕНДЛЕРЫ ======
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Я помогу купить *сертификат разработчика iPhone* 🍎",
        reply_markup=main_menu()
    )

@dp.message(lambda m: m.text == "🛒 Купить сертификат")
async def choose_cert(message: types.Message):
    await message.answer(
        "📦 *Выберите сертификат:*",
        reply_markup=cert_menu()
    )

@dp.message(lambda m: m.text in [
    "🔹 Обычный — 250₽",
    "🔹 Super обычный — 350₽",
    "🍎 Мгновенный — 500₽",
    "⚡ Super мгновенный — 700₽",
    "🍎 Ultra мгновенный — 2000₽"
])
async def pay_info(message: types.Message):
    await message.answer(
        CARD_TEXT,
        reply_markup=pay_menu()
    )

@dp.message(lambda m: m.text == "💳 Я оплатил")
async def paid(message: types.Message):
    await message.answer(
        "✅ *Спасибо!*\n\n"
        "Я передал информацию администратору.\n"
        "Он скоро с вами свяжется 👇\n\n"
        f"{ADMIN_USERNAME}"
    )

@dp.message(lambda m: m.text in ["⬅️ Назад", "⬅️ Назад к выбору"])
async def back(message: types.Message):
    await message.answer(
        "📦 *Выберите сертификат:*",
        reply_markup=cert_menu()
    )

# ====== ЗАПУСК ======
async def main():
    print("Бот запущен и работает")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
