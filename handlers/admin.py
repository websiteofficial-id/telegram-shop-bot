from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import ADMIN_ID
from database import products, orders, add_product, delete_product

def is_admin(update):
    return update.effective_user and update.effective_user.id == ADMIN_ID

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return await update.message.reply_text("⛔ Kamu bukan admin.")
    kb=[
        [InlineKeyboardButton("📊 Statistik",callback_data="admin:stats")],
        [InlineKeyboardButton("📦 Produk",callback_data="admin:products")],
        [InlineKeyboardButton("🧾 Pesanan",callback_data="admin:orders")]
    ]
    await update.message.reply_text("👑 PANEL ADMIN",reply_markup=InlineKeyboardMarkup(kb))

async def admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    await update.message.reply_text("Gunakan /admin untuk membuka panel admin.")

async def handle_admin_callback(update, context):
    q=update.callback_query
    if q.from_user.id != ADMIN_ID:
        await q.answer("Akses ditolak.",show_alert=True); return
    await q.answer()
