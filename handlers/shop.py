from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import products, add_order

def rupiah(n):
    return f"Rp{n:,}".replace(",", ".")

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_shop(update, context)

async def show_shop(update, context):
    rows=products()
    buttons=[]
    for p in rows:
        pid,name,desc,price,stock,cat=p
        buttons.append([InlineKeyboardButton(
            f"🛒 {name} — {rupiah(price)}",
            callback_data=f"product:{pid}"
        )])
    text="🛍️ KATALOG TOKO\n\nPilih produk:"
    markup=InlineKeyboardMarkup(buttons or [[InlineKeyboardButton("Belum ada produk",callback_data="noop")]])
    if update.callback_query:
        await update.callback_query.edit_message_text(text,reply_markup=markup)
    else:
        await update.message.reply_text(text,reply_markup=markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query
    await q.answer()
    data=q.data

    if data=="shop":
        return await show_shop(update,context)

    if data.startswith("product:"):
        pid=int(data.split(":")[1])
        p=next((x for x in products() if x[0]==pid),None)
        if not p:
            return await q.edit_message_text("Produk tidak ditemukan.")
        _,name,desc,price,stock,cat=p
        kb=[[InlineKeyboardButton("🛒 Beli 1",callback_data=f"buy:{pid}")],
            [InlineKeyboardButton("⬅️ Kembali",callback_data="shop")]]
        await q.edit_message_text(
            f"📦 {name}\n\n{desc}\n\nKategori: {cat}\nHarga: {rupiah(price)}\nStok: {stock}",
            reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("buy:"):
        pid=int(data.split(":")[1])
        p=next((x for x in products() if x[0]==pid),None)
        if not p or p[4] <= 0:
            return await q.edit_message_text("❌ Stok produk habis.")
        _,name,desc,price,stock,cat=p
        oid=add_order(q.from_user.id, q.from_user.username or "-", f"{name} x1", price)
        await q.edit_message_text(
            f"✅ Pesanan dibuat!\n\nOrder #{oid}\nProduk: {name}\nTotal: {rupiah(price)}\nStatus: Pending\n\nAdmin akan memproses pesananmu."
        )
        return

    if data=="myorders":
        await q.edit_message_text("📦 Fitur riwayat pesanan siap digunakan pada versi pengembangan berikutnya.")
