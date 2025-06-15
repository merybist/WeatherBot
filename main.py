import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from handlers.weather_module import WeatherHandler
from db import init_db, upsert_user, get_user_language, set_user_language

init_db()

load_dotenv()

bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()
weather_handler = WeatherHandler()

TEXTS = {
    'uk': {
        'welcome': "👋 Вітаю! Я бот прогнозу погоди.\n\nПросто напишіть назву міста, і я покажу вам прогноз погоди на тиждень.\nНаприклад: Київ, Львів, Одеса",
        'help': "📖 Як користуватися ботом:\n\n1. Просто напишіть назву міста\n2. Отримайте детальний прогноз погоди на тиждень\n\nДоступні команди:\n/start - Почати роботу з ботом\n/help - Показати це повідомлення\n/language - Змінити мову",
        'wait': "⏳ Отримую прогноз погоди...",
        'choose_lang': "Оберіть мову / Choose language:",
        'lang_set': "Мову змінено на українську 🇺🇦",
        'unknown': "Не вдалося розпізнати місто. Спробуйте ще раз."
    },
    'en': {
        'welcome': "👋 Hi! I'm a weather forecast bot.\n\nJust type the name of a city and I'll show you the weekly weather forecast.\nFor example: Kyiv, Lviv, Odesa",
        'help': "📖 How to use the bot:\n\n1. Just type a city name\n2. Get a detailed weekly weather forecast\n\nAvailable commands:\n/start - Start using the bot\n/help - Show this message\n/language - Change language",
        'wait': "⏳ Getting the weather forecast...",
        'choose_lang': "Оберіть мову / Choose language:",
        'lang_set': "Language set to English 🇬🇧",
        'unknown': "Could not recognize the city. Please try again."
    }
}

lang_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Українська 🇺🇦"), KeyboardButton(text="English 🇬🇧")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    upsert_user(message.from_user.id, message.from_user.username)
    lang = get_user_language(message.from_user.id)
    await message.answer(TEXTS[lang]['welcome'])

@dp.message(Command("help"))
async def cmd_help(message: Message):
    upsert_user(message.from_user.id, message.from_user.username)
    lang = get_user_language(message.from_user.id)
    await message.answer(TEXTS[lang]['help'])

@dp.message(Command("language"))
async def cmd_language(message: Message):
    upsert_user(message.from_user.id, message.from_user.username)
    lang = get_user_language(message.from_user.id)
    await message.answer(TEXTS[lang]['choose_lang'], reply_markup=lang_keyboard)

@dp.message(lambda m: m.text in ["Українська 🇺🇦", "English 🇬🇧"])
async def set_language_cmd(message: Message):
    lang = 'uk' if message.text == "Українська 🇺🇦" else 'en'
    set_user_language(message.from_user.id, lang)
    upsert_user(message.from_user.id, message.from_user.username, lang)
    await message.answer(TEXTS[lang]['lang_set'], reply_markup=types.ReplyKeyboardRemove())

@dp.message()
async def handle_message(message: Message):
    upsert_user(message.from_user.id, message.from_user.username)
    lang = get_user_language(message.from_user.id)
    city = message.text.strip()
    await message.answer(TEXTS[lang]['wait'])
    forecast = weather_handler.get_weather_forecast(city, lang=lang)
    await message.answer(forecast)

async def main():
    init_db()
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
