import os
from dotenv import load_dotenv


# Membaca file .env jika tersedia
load_dotenv()


# =========================
# BOT CONFIGURATION
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

ADMIN_ID_RAW = os.getenv("ADMIN_ID", "0").strip()

try:
    ADMIN_ID = int(ADMIN_ID_RAW)
except ValueError:
    ADMIN_ID = 0
