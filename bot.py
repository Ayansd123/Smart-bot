import os
import asyncio
from aiohttp import web
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает 24/7.")

async def handle(request):
    app = request.app["bot_app"]
    data = await request.json()
    update = Update.de_json(data, app.bot)
    await app.process_update(update)
    return web.Response(text="ok")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    await app.initialize()

    # Получаем URL Render
    render_url = os.getenv("RENDER_EXTERNAL_URL")

    # Устанавливаем webhook с явным путем
    await app.bot.set_webhook(url=f"{render_url}/")

    await app.start()

    web_app = web.Application()
    web_app["bot_app"] = app
    web_app.router.add_post("/", handle)

    port = int(os.environ.get("PORT", 10000))

    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
