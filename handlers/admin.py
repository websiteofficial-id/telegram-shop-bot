from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import ADMIN_ID
from database import products, orders, add_product, delete_product


def is_admin(update: Update) -> bool:
    """Memeriksa apakah pengguna adalah admin."""
    return (
        update.effective_user is not None
        and update.effective_user.id == ADMIN_ID
    )


def rupiah(amount: int) -> str:
    """Format angka menjadi Rupiah."""
    return f"Rp{amount:,}".replace(",", ".")


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Membuka panel admin."""
    if not is_admin(update):
        await update.message.reply_text("⛔ Akses ditolak.")
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "📊 Statistik",
                callback_data="admin:stats"
            )
        ],
        [
            InlineKeyboardButton(
                "📦 Kelola Produk",
                callback_data="admin:products"
            )
        ],
        [
            InlineKeyboardButton(
                "🧾 Pesanan",
                callback_data="admin:orders"
            )
        ],
    ]

    await update.message.reply_text(
        "👑 PANEL ADMIN TOKO\n\n"
        "Selamat datang di panel administrator.\n"
        "Pilih menu yang ingin kamu kelola:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def handle_admin_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Menangani tombol-tombol panel admin."""

    query = update.callback_query

    if query.from_user.id != ADMIN_ID:
        await query.answer(
            "⛔ Kamu bukan admin!",
            show_alert=True
        )
        return

    await query.answer()

    data = query.data

    # =========================
    # STATISTIK
    # =========================
    if data == "admin:stats":

        product_list = products()
        order_list = orders()

        total_products = len(product_list)
        total_orders = len(order_list)

        total_stock = sum(
            product[4]
            for product in product_list
        )

        total_revenue = sum(
            order[4]
            for order in order_list
            if order[5] != "Dibatalkan"
        )

        text = (
            "📊 STATISTIK TOKO\n\n"
            f"📦 Total produk: {total_products}\n"
            f"📋 Total pesanan: {total_orders}\n"
            f"📊 Total stok: {total_stock}\n"
            f"💰 Pendapatan: {rupiah(total_revenue)}"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "⬅️ Kembali",
                    callback_data="admin:menu"
                )
            ]
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # =========================
    # DAFTAR PRODUK
    # =========================
    if data == "admin:products":

        product_list = products()

        if not product_list:
            text = "📦 PRODUK\n\nBelum ada produk."
        else:
            lines = ["📦 DAFTAR PRODUK\n"]

            for product in product_list:
                (
                    product_id,
                    name,
                    description,
                    price,
                    stock,
                    category
                ) = product

                lines.append(
                    f"#{product_id} — {name}\n"
                    f"💰 {rupiah(price)}\n"
                    f"📦 Stok: {stock}\n"
                    f"🏷️ Kategori: {category}\n"
                )

            text = "\n".join(lines)

        keyboard = [
            [
                InlineKeyboardButton(
                    "➕ Tambah Produk",
                    callback_data="admin:add_product"
                )
            ],
            [
                InlineKeyboardButton(
                    "🗑️ Hapus Produk",
                    callback_data="admin:delete_product"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Kembali",
                    callback_data="admin:menu"
                )
            ]
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # =========================
    # DAFTAR PESANAN
    # =========================
    if data == "admin:orders":

        order_list = orders()

        if not order_list:
            text = "🧾 PESANAN\n\nBelum ada pesanan."
        else:
            lines = ["🧾 PESANAN TERBARU\n"]

            for order in order_list[:15]:

                (
                    order_id,
                    user_id,
                    username,
                    items,
                    total,
                    status,
                    created_at
                ) = order

                lines.append(
                    f"🧾 Order #{order_id}\n"
                    f"👤 @{username}\n"
                    f"🛍️ {items}\n"
                    f"💰 {rupiah(total)}\n"
                    f"📌 Status: {status}\n"
                    f"🕒 {created_at}\n"
                )

            text = "\n".join(lines)

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔄 Refresh",
                    callback_data="admin:orders"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Kembali",
                    callback_data="admin:menu"
                )
            ]
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # =========================
    # TAMBAH PRODUK
    # =========================
    if data == "admin:add_product":

        context.user_data["admin_action"] = "add_product"

        await query.edit_message_text(
            "➕ TAMBAH PRODUK\n\n"
            "Kirim data produk dengan format:\n\n"
            "Nama | Deskripsi | Harga | Stok | Kategori\n\n"
            "Contoh:\n"
            "Keyboard Gaming | Keyboard RGB | 150000 | 10 | Gaming"
        )
        return

    # =========================
    # HAPUS PRODUK
    # =========================
    if data == "admin:delete_product":

        context.user_data["admin_action"] = "delete_product"

        await query.edit_message_text(
            "🗑️ HAPUS PRODUK\n\n"
            "Kirim ID produk yang ingin dihapus.\n\n"
            "Contoh:\n"
            "3"
        )
        return

    # =========================
    # MENU ADMIN
    # =========================
    if data == "admin:menu":

        keyboard = [
            [
                InlineKeyboardButton(
                    "📊 Statistik",
                    callback_data="admin:stats"
                )
            ],
            [
                InlineKeyboardButton(
                    "📦 Kelola Produk",
                    callback_data="admin:products"
                )
            ],
            [
                InlineKeyboardButton(
                    "🧾 Pesanan",
                    callback_data="admin:orders"
                )
            ],
        ]

        await query.edit_message_text(
            "👑 PANEL ADMIN TOKO\n\n"
            "Pilih menu:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return


async def admin_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Menangani input teks dari admin."""

    if not is_admin(update):
        return

    action = context.user_data.get("admin_action")

    # =========================
    # TAMBAH PRODUK
    # =========================
    if action == "add_product":

        try:
            parts = [
                item.strip()
                for item in update.message.text.split("|")
            ]

            if len(parts) != 5:
                raise ValueError

            name = parts[0]
            description = parts[1]
            price = int(parts[2])
            stock = int(parts[3])
            category = parts[4]

            if price < 0 or stock < 0:
                raise ValueError

            add_product(
                name,
                description,
                price,
                stock,
                category
            )

            context.user_data.pop("admin_action", None)

            await update.message.reply_text(
                "✅ PRODUK BERHASIL DITAMBAHKAN!\n\n"
                f"📦 Nama: {name}\n"
                f"💰 Harga: {rupiah(price)}\n"
                f"📊 Stok: {stock}\n"
                f"🏷️ Kategori: {category}"
            )

        except (ValueError, TypeError):
            await update.message.reply_text(
                "❌ Format salah.\n\n"
                "Gunakan:\n"
                "Nama | Deskripsi | Harga | Stok | Kategori\n\n"
                "Contoh:\n"
                "Keyboard Gaming | Keyboard RGB | 150000 | 10 | Gaming"
            )

        return

    # =========================
    # HAPUS PRODUK
    # =========================
    if action == "delete_product":

        try:
            product_id = int(update.message.text.strip())

            delete_product(product_id)

            context.user_data.pop("admin_action", None)

            await update.message.reply_text(
                f"✅ Produk #{product_id} berhasil dihapus."
            )

        except ValueError:
            await update.message.reply_text(
                "❌ ID produk harus berupa angka."
            )

        return

    await update.message.reply_text(
        "👑 Gunakan /admin untuk membuka panel admin."
    )
