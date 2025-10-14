#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
businka_feed_bot_full.py
========================

🐾 Businka Feed Bot — Telegram-бот для напоминания о кормлении питомца.

Автор: NK
GitHub: https://github.com/Cayman152
Лицензия: MIT © 2025 NK

Перед запуском:
1. Установите зависимости из requirements.txt
2. Установите переменную окружения BOT_TOKEN со значением вашего токена Telegram-бота
3. Запустите: python3 businka_feed_bot_full.py
"""

import os
import asyncio
import json
import random
from datetime import datetime, date, timedelta
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    Message, CallbackQuery,
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# -----------------------------------------------------------------------------
# 🔧 Конфигурация
# -----------------------------------------------------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# -----------------------------------------------------------------------------
# 💾 Работа с данными
# -----------------------------------------------------------------------------
DATA_FILE = "businka_data.json"
DEFAULT_NAME = "Бусинка"
DEFAULT_FEED_TIMES = ["09:00", "13:00", "18:00"]


def load_data():
    """Загрузка данных питомца из файла JSON."""
    if not os.path.exists(DATA_FILE):
        return {"pet_name": DEFAULT_NAME, "feed_times": DEFAULT_FEED_TIMES, "weight_history": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    """Сохранение данных питомца в файл JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


data = load_data()
pet_name = data["pet_name"]
feed_times = data["feed_times"]

# -----------------------------------------------------------------------------
# 📅 Состояния FSM
# -----------------------------------------------------------------------------
class Form(StatesGroup):
    waiting_for_new_name = State()
    waiting_for_feed_time = State()
    waiting_for_weight = State()


# -----------------------------------------------------------------------------
# 🧠 Вспомогательные функции
# -----------------------------------------------------------------------------
def get_today_date_str():
    """Возвращает текущую дату в формате ГГГГ-ММ-ДД."""
    return date.today().strftime("%Y-%m-%d")


def format_weight_history():
    """Форматирует историю веса в красивый текст."""
    if not data["weight_history"]:
        return "История веса пока пуста 🐾"
    lines = [f"{w['date']}: {w['weight']} кг" for w in data["weight_history"][-10:]]
    return "\n".join(lines)


# -----------------------------------------------------------------------------
# ⚙️ Команды
# -----------------------------------------------------------------------------
@dp.message(Command("start"))
async def start_handler(message: Message):
    """Приветствие и основное меню."""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍽️ Кормление"), KeyboardButton(text="⚖️ Взвешивание")],
            [KeyboardButton(text="⏰ Настройки"), KeyboardButton(text="📜 История веса")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        f"Привет, {message.from_user.first_name}! 🐾\n"
        f"Я помогу тебе заботиться о {pet_name}.",
        reply_markup=kb
    )


@dp.message(F.text == "🍽️ Кормление")
async def feed_handler(message: Message):
    """Напоминание о кормлении."""
    now = datetime.now().strftime("%H:%M")
    await message.answer(f"⏰ Сейчас {now}. Не забудь покормить {pet_name}! 🐱")


@dp.message(F.text == "⚖️ Взвешивание")
async def weight_handler(message: Message, state: FSMContext):
    """Запрос нового значения веса."""
    await message.answer("Введи вес питомца в килограммах (например: 4.5):")
    await state.set_state(Form.waiting_for_weight)


@dp.message(Form.waiting_for_weight)
async def process_weight(message: Message, state: FSMContext):
    """Сохранение нового веса."""
    try:
        weight = float(message.text.replace(",", "."))
        record = {"date": get_today_date_str(), "weight": weight}
        data["weight_history"].append(record)
        save_data(data)
        await message.answer(f"✅ Вес {pet_name} сохранён: {weight} кг")
    except ValueError:
        await message.answer("Пожалуйста, введи число, например 4.2")
    await state.clear()


@dp.message(F.text == "📜 История веса")
async def history_handler(message: Message):
    """Отправка истории веса."""
    await message.answer(format_weight_history())


@dp.message(F.text == "⏰ Настройки")
async def settings_handler(message: Message):
    """Меню настроек."""
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Изменить имя 🐾", callback_data="change_name")],
            [InlineKeyboardButton(text="Изменить время кормления ⏰", callback_data="change_feed_time")]
        ]
    )
    await message.answer("Выбери, что хочешь изменить:", reply_markup=kb)


# -----------------------------------------------------------------------------
# 🔧 Callback-обработчики
# -----------------------------------------------------------------------------
@dp.callback_query(F.data == "change_name")
async def change_name_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введи новое имя питомца:")
    await state.set_state(Form.waiting_for_new_name)
    await callback.answer()


@dp.message(Form.waiting_for_new_name)
async def process_new_name(message: Message, state: FSMContext):
    """Изменение имени питомца."""
    global pet_name
    pet_name = message.text.strip()
    data["pet_name"] = pet_name
    save_data(data)
    await message.answer(f"Имя питомца изменено на {pet_name} 🐾")
    await state.clear()


@dp.callback_query(F.data == "change_feed_time")
async def change_feed_time_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введи новое время кормления (например: 10:30, 14:00, 19:00):")
    await state.set_state(Form.waiting_for_feed_time)
    await callback.answer()


@dp.message(Form.waiting_for_feed_time)
async def process_feed_time(message: Message, state: FSMContext):
    """Изменение времени кормления."""
    times = [t.strip() for t in message.text.split(",") if t.strip()]
    global feed_times
    feed_times = times
    data["feed_times"] = feed_times
    save_data(data)
    await message.answer(f"Новое время кормлений установлено: {', '.join(feed_times)} ⏰")
    await state.clear()


# -----------------------------------------------------------------------------
# 🚀 Основной запуск
# -----------------------------------------------------------------------------
async def main():
    """Запуск бота."""
    print("🐾 Businka Feed Bot запущен и готов к работе!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
