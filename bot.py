import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import BOT_TOKEN
from database import init_db
from handlers.start import start
from handlers.shop import shop, button_handler
from handlers.admin import admin, admin_text

logging.basicConfig(level=logging.INFO)

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN belum diatur di .env")
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("shop", shop))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, admin_text))
    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
