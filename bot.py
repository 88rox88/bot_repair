from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from database import save_request
from config import TOKEN

# Состояния для диалога
USERNAME, CONTACT, ISSUE, TIME = range(4)


async def start(update: Update, context):
    await update.message.reply_text("Привет! Я бот для сбора заявок на ремонт бытовой техники. Как тебя зовут?")
    return USERNAME


async def get_username(update: Update, context):
    context.user_data["username"] = update.message.text
    await update.message.reply_text("Спасибо! Теперь введи свой контактный номер или Telegram-ник.")
    return CONTACT


async def get_contact(update: Update, context):
    context.user_data["contact"] = update.message.text
    await update.message.reply_text("Опиши проблему, например: 'Не отжимает стиральная машина'.")
    return ISSUE


async def get_issue(update: Update, context):
    context.user_data["issue"] = update.message.text
    await update.message.reply_text("Когда тебе удобно, чтобы с тобой связались? (например, 'с 14:00 до 18:00')")
    return TIME


async def get_time(update: Update, context):
    context.user_data["preferred_time"] = update.message.text

    # Сохраняем в базу данных
    save_request(
        context.user_data["username"],
        context.user_data["contact"],
        context.user_data["issue"],
        context.user_data["preferred_time"]
    )

    await update.message.reply_text("Заявка принята! С тобой свяжутся в удобное время.")
    return ConversationHandler.END


async def cancel(update: Update, context):
    await update.message.reply_text("Операция отменена.")
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_username)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_contact)],
            ISSUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_issue)],
            TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv_handler)

    print("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
