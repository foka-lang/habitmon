import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, PreCheckoutQueryHandler, \
    MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# ============================================================
# ТОКЕН ИЗ ПЕРЕМЕННОЙ ОКРУЖЕНИЯ
# ============================================================
BOT_TOKEN = os.getenv('BOT_TOKEN')
PROVIDER_TOKEN = ""  # Для цифровых товаров оставляем ПУСТЫМ

# Ссылка на Mini App
MINI_APP_URL = "https://foka-lang.github.io/habitmon/"


# ============================================================
# КОМАНДА /start
# ============================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

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

    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')


# ============================================================
# ОТПРАВКА СЧЕТА
# ============================================================
async def send_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE, plan: str):
    """Отправляет счёт на оплату в Stars."""

    prices = {
        "trial": [LabeledPrice("Пробный (3 дня)", 0)],
        "basic": [LabeledPrice("Обычная (30 дней)", 6100)],
        "premium": [LabeledPrice("Премиум (30 дней)", 12200)]
    }

    titles = {
        "trial": "Пробный период HabitMon",
        "basic": "Обычная подписка HabitMon",
        "premium": "Премиум подписка HabitMon"
    }

    descriptions = {
        "trial": "3 дня бесплатного доступа. 15 привычек.",
        "basic": "30 дней доступа. 15 привычек.",
        "premium": "30 дней доступа. 50 привычек."
    }

    await update.callback_query.message.reply_invoice(
        title=titles[plan],
        description=descriptions[plan],
        payload=f"subscription_{plan}",
        provider_token=PROVIDER_TOKEN,
        currency="XTR",
        prices=prices[plan],
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        is_flexible=False
    )


# ============================================================
# ПРОВЕРКА ПЛАТЕЖА
# ============================================================
async def pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


# ============================================================
# УСПЕШНАЯ ОПЛАТА
# ============================================================
async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payment = update.message.successful_payment
    plan = payment.invoice_payload.replace("subscription_", "")

    plan_names = {
        "trial": "Пробный (3 дня)",
        "basic": "Обычная (30 дней)",
        "premium": "Премиум (30 дней)"
    }

    await update.message.reply_text(
        f"✅ **Оплата прошла успешно!**\n\n"
        f"📦 Тариф: {plan_names.get(plan, 'Неизвестный')}\n"
        f"⭐ Оплачено: {payment.total_amount / 100} Stars\n\n"
        "🎉 Подписка активирована!",
        parse_mode='Markdown'
    )


# ============================================================
# ОБРАБОТКА КНОПОК
# ============================================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "subscription":
        keyboard = [
            [InlineKeyboardButton("🔹 Пробный (0 ★)", callback_data="sub_trial")],
            [InlineKeyboardButton("🔸 Обычная (61 ★)", callback_data="sub_basic")],
            [InlineKeyboardButton("⭐ Премиум (122 ★)", callback_data="sub_premium")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
        ]
        await query.edit_message_text(
            "💎 **Выберите тариф**\n\n"
            "🔹 **Пробный** — 3 дня бесплатно, 15 привычек\n"
            "🔸 **Обычная** — 30 дней, 61 ★, 15 привычек\n"
            "⭐ **Премиум** — 30 дней, 122 ★, 50 привычек",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    elif data.startswith("sub_"):
        plan = data.replace("sub_", "")
        await send_invoice(update, context, plan)

    elif data == "back_to_menu":
        await start(update, context)

    elif data == "progress":
        await query.edit_message_text(
            "📊 **Мой прогресс**\n\nСкоро здесь появится статистика! 🚀",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ]),
            parse_mode='Markdown'
        )
    elif data == "rating":
        await query.edit_message_text(
            "🏆 **Рейтинг**\n\nСкоро здесь появится рейтинг!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ]),
            parse_mode='Markdown'
        )
    elif data == "referral":
        await query.edit_message_text(
            "👥 **Реферальная программа**\n\nСкоро здесь появится реферальная ссылка!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ]),
            parse_mode='Markdown'
        )


# ============================================================
# ЗАПУСК
# ============================================================
def main():
    if not BOT_TOKEN:
        print("❌ Ошибка: BOT_TOKEN не найден! Проверь .env или Render!")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(PreCheckoutQueryHandler(pre_checkout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

    print("🤖 Бот HabitMon запущен и готов к работе!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
