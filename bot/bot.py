import os
import sys
import logging
import json
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Добавляем путь к backend, чтобы импортировать Config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Пытаемся импортировать Config, если есть
try:
    from backend.config import Config
    BOT_TOKEN = Config.BOT_TOKEN
except:
    BOT_TOKEN = os.getenv('BOT_TOKEN')

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Ссылка на Mini App
MINI_APP_URL = "https://foka-lang.github.io/habitmon/"

# ============================================================
# КОМАНДА /start
# ============================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Создаём клавиатуру
    keyboard = [
        [InlineKeyboardButton("🎮 Открыть трекер", web_app={"url": MINI_APP_URL})],
        [InlineKeyboardButton("💎 Подписка", callback_data="subscription")],
        [InlineKeyboardButton("📊 Мой прогресс", callback_data="progress")],
        [InlineKeyboardButton("🏆 Рейтинг", callback_data="rating")],
        [InlineKeyboardButton("👥 Пригласить друга", callback_data="referral")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        f"👋 Привет, {user.first_name}!\n\n"
        "🐾 Я **HabitMon** — твой помощник в мире привычек!\n\n"
        "Я помогу тебе:\n"
        "✅ Отслеживать ежедневные привычки\n"
        "🏆 Соревноваться с друзьями\n"
        "🎁 Зарабатывать баллы и повышать уровень\n\n"
        "👉 Нажми «Открыть трекер», чтобы начать!\n"
        "💎 Нажми «Подписка», чтобы выбрать тариф."
    )

    if update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# ============================================================
# ОБРАБОТКА КНОПОК
# ============================================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "progress":
        await query.edit_message_text(
            "📊 **Мой прогресс**\n\n"
            "Здесь ты увидишь свою статистику:\n"
            "• Количество выполненных привычек\n"
            "• Текущая серия дней\n"
            "• Максимальная серия\n"
            "• Всего выполнено за всё время\n\n"
            "Скоро здесь появится детальная статистика! 🚀",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ]),
            parse_mode='Markdown'
        )

    elif data == "rating":
        await query.edit_message_text(
            "🏆 **Рейтинг**\n\n"
            "1️⃣ Алексей — 45 ✅\n"
            "2️⃣ Мария — 42 ✅\n"
            "3️⃣ Игорь — 38 ✅\n"
            "4️⃣ Ольга — 30 ✅\n"
            "5️⃣ Сергей — 28 ✅\n\n"
            "Ты пока не в топе, но у тебя всё впереди! 💪",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ]),
            parse_mode='Markdown'
        )

    elif data == "referral":
        await query.edit_message_text(
            "👥 **Реферальная программа**\n\n"
            "Приглашай друзей и получай бонусы!\n"
            "За каждого друга ты получишь **250 баллов**! 🎁\n\n"
            "Твоя реферальная ссылка появится здесь позже.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ]),
            parse_mode='Markdown'
        )

    elif data == "subscription":
        keyboard = [
            [InlineKeyboardButton("🔹 Пробный (3 дня)", callback_data="sub_trial")],
            [InlineKeyboardButton("🔸 Обычная (61 ★)", callback_data="sub_basic")],
            [InlineKeyboardButton("⭐ Премиум (122 ★)", callback_data="sub_premium")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
        ]
        await query.edit_message_text(
            "💎 **Выберите тариф подписки**\n\n"
            "🔹 **Пробный** — 3 дня бесплатно, 15 привычек\n"
            "🔸 **Обычная** — 30 дней, 61 ★, 15 привычек\n"
            "⭐ **Премиум** — 30 дней, 122 ★, 50 привычек\n\n"
            "Выберите подходящий вариант:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    elif data == "sub_trial":
        # Активируем пробную подписку
        await query.edit_message_text(
            "✅ **Пробный период активирован!**\n\n"
            "🎉 Ты получил 3 дня бесплатного доступа!\n"
            "📊 Доступно: 15 привычек\n\n"
            "👉 Открой трекер и начни развивать привычки!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎮 Открыть трекер", web_app={"url": MINI_APP_URL})],
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ]),
            parse_mode='Markdown'
        )

    elif data == "sub_basic":
        # Здесь будет логика оплаты через Stars
        await query.edit_message_text(
            "💎 **Обычная подписка**\n\n"
            "💰 Стоимость: 61 ★\n"
            "📅 Срок: 30 дней\n"
            "📊 Доступно: 15 привычек\n\n"
            "Скоро здесь появится кнопка оплаты через Telegram Stars! 🌟",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="subscription")]
            ]),
            parse_mode='Markdown'
        )

    elif data == "sub_premium":
        await query.edit_message_text(
            "⭐ **Премиум подписка**\n\n"
            "💰 Стоимость: 122 ★\n"
            "📅 Срок: 30 дней\n"
            "📊 Доступно: 50 привычек\n\n"
            "Скоро здесь появится кнопка оплаты через Telegram Stars! 🌟",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="subscription")]
            ]),
            parse_mode='Markdown'
        )

    elif data == "back_to_menu":
        await start(update, context)

# ============================================================
# ЗАПУСК
# ============================================================
def main():
    if not BOT_TOKEN:
        print("❌ Ошибка: BOT_TOKEN не найден!")
        return

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Бот HabitMon запущен и готов к работе!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
