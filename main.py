"""
🇩🇪 Nemis Tili AI Bot - Telegram Bot
O'zbek tilida nemis tilini o'rganish uchun AI yordamchi
"""
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

from config import TELEGRAM_BOT_TOKEN
from handlers.commands import start_command, help_command, admin_command, stats_command
from handlers.messages import handle_message
from handlers.callbacks import handle_callback

# Logging sozlamalari
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xatoliklarni qayta ishlash"""
    logger.error(f"Xatolik: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Xatolik yuz berdi. Iltimos, qayta urinib koring."
        )


def main():
    """Botni ishga tushirish"""
    logger.info("Bot ishga tushirilmoqda...")

    # Application yaratish
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command handlerlar
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("stats", stats_command))

    # Callback handler
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Message handler (barcha matnli xabarlar)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Xatolik handleri
    application.add_error_handler(error_handler)

    # Botni ishga tushirish
    logger.info("Bot ishga tushdi!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
