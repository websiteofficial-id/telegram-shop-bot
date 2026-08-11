# Telegram Shop Bot

Bot toko Telegram berbasis Python.

## Fitur awal
- Katalog produk
- Detail produk
- Pembelian sederhana
- Order ID otomatis
- Panel admin
- Database SQLite
- Siap dijalankan dengan polling di Railway

## Menjalankan lokal
1. Salin `.env.example` menjadi `.env`
2. Isi `BOT_TOKEN`
3. Isi `ADMIN_ID`
4. Install dependency:
   `pip install -r requirements.txt`
5. Jalankan:
   `python bot.py`

## Railway
Gunakan Start Command:
`python bot.py`

Tambahkan Variables:
- `BOT_TOKEN`
- `ADMIN_ID`

Jangan upload file `.env` yang berisi token bot ke GitHub.
