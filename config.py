"""
Bot konfiguratsiyasi
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-70b-versatile"  # yoki "mixtral-8x7b-32768"

# Bot sozlamalari
BOT_NAME = "🇩🇪 Nemis Tili AI Bot"
DEFAULT_LANGUAGE = "uz"

# Darajalar
LEVELS = {
    "beginner": "A1 - Boshlang'ich",
    "elementary": "A2 - Oddiy",
    "intermediate": "B1 - O'rta",
    "upper_intermediate": "B2 - Yuqori o'rta",
    "advanced": "C1 - Yuqori"
}

# Xatolik xabarlari
ERROR_MESSAGES = {
    "uz": "❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.",
    "de": "❌ Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut."
}
