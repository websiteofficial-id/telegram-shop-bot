import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN
from database import init_db

from handlers.start import start
from handlers.shop import shop, button_handler
from handlers.admin import (
    admin,
    admin_text,
    handle_admin_callback,
)


# =========================
# LOGGING
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# =========================
# ERROR HANDLER
# =========================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):
    logger.error(
        "Terjadi error:",
        exc_info=context.error
    )


# =========================
# MAIN
# =========================

def main():

    # Cek token bot
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN belum diatur di Environment Variables."
        )

    # Membuat database jika belum ada
    init_db()

    # Membuat aplikasi Telegram
    app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    # =========================
    # COMMAND USER
    # =========================

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CommandHandler(
            "shop",
            shop
        )
    )

    # =========================
    # COMMAND ADMIN
    # =========================

    app.add_handler(
        CommandHandler(
            "admin",
            admin
        )
    )

    # =========================
    # CALLBACK TOKO
    # =========================

    app.add_handler(
        CallbackQueryHandler(
            button_handler,
            pattern=r"^(shop|product:|buy:|myorders)"
        )
    )

    # =========================
    # CALLBACK ADMIN
    # =========================

    app.add_handler(
        CallbackQueryHandler(
            handle_admin_callback,
            pattern=r"^admin:"
        )
    )

    # =========================
    # PESAN TEKS
    # =========================

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            admin_text
        )
    )

    # =========================
    # ERROR HANDLER
    # =========================

    app.add_error_handler(
        error_handler
    )

    print("================================")
    print("🤖 TELEGRAM SHOP BOT")
    print("================================")
    print("✅ Bot berhasil dijalankan.")
    print("📡 Menunggu pesan Telegram...")
    print("================================")

    # Jalankan bot
    app.run_polling(
        drop_pending_updates=True
    )


# =========================
# START PROGRAM
# =========================

if __name__ == "__main__":
    main()
