from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard=[
        [InlineKeyboardButton("🛍️ Buka Toko", callback_data="shop")],
        [InlineKeyboardButton("📦 Pesanan Saya", callback_data="myorders")]
    ]
    await update.message.reply_text(
        "👋 Selamat datang di toko!\n\nPilih menu di bawah:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
