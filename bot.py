import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = "7989675191:AAHcGwm5C8rUSCLP8YDrDPahw2_ulLM-1EA"

async def main():
    print("Бот запускается...")

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(message: Message):
        await message.answer("✅ Бот запущен и отвечает на /start")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
