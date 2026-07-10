import os
import sys
import logging
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
        "👉 Нажми «Открыть трекер», чтобы начать!"
    )

    # Проверяем, откуда пришёл запрос
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