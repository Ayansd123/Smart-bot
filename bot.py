from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text("Бот работает 24/7.")

async def echo(update, context):
    await update.message.reply_text("Ты написал: " + update.message.text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()
