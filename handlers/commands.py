"""
Asosiy buyruqlar handlerlari
"""
from telegram import Update
from telegram.ext import ContextTypes
from config import BOT_NAME, ADMIN_ID
from utils.database import create_user, get_user, update_user, get_stats
from utils.keyboards import get_main_menu, get_levels_menu, get_admin_menu
from utils.groq_client import groq


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start buyrug'i"""
    user = update.effective_user
    user_id = user.id

    # Foydalanuvchini tekshirish yoki yaratish
    existing_user = get_user(user_id)
    if not existing_user:
        create_user(user_id, user.username, user.first_name)
    else:
        update_user(user_id, last_active=__import__("datetime").datetime.now().isoformat())

    welcome_text = f"""
🇩🇪 <b>{BOT_NAME}</b> ga xush kelibsiz, {user.first_name}!

Men sizning shaxsiy nemis tili o'qituvchingizman. Quyidagi imkoniyatlarga ega:

📚 <b>Darslar</b> - Grammatika, suhbatlar, matnlar
🔄 <b>Tarjima</b> - O'zbek ↔ Nemis
💬 <b>Suhbat</b> - AI bilan suhbat mashqi
📝 <b>Mashq</b> - Testlar va mashqlar
📊 <b>Daraja</b> - O'z bilimingizni tekshiring

<b>Qanday boshlash kerak?</b>
1. "📊 Daraja" tugmasini bosing
2. O'z darajangizni tanlang
3. "🇩🇪 Darslar" dan boshlang!

<i>Bot Groq AI (Llama 3.1) yordamida ishlaydi</i>
"""

    await update.message.reply_text(
        welcome_text,
        parse_mode="HTML",
        reply_markup=get_main_menu()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/help buyrug'i"""
    help_text = """
<b>📖 Botdan foydalanish qo'llanmasi:</b>

<b>🇩🇪 Darslar</b>
Grammatika, suhbatlar, matnlar va tinglash mashqlari

<b>🔄 Tarjima</b>
O'zbek tilidan nemis tiliga va aksincha tarjima

<b>💬 Suhbat</b>
AI bilan turli vaziyatlarda suhbat qilish mashqi

<b>📝 Mashq</b>
Testlar, so'z yig'ini va grammatika mashqlari

<b>📊 Daraja</b>
O'z bilim darajangizni aniqlang (A1-C1)

<b>⚙️ Sozlamalar</b>
Bildirishnomalar va boshqa sozlamalar

<b>Buyruqlar:</b>
/start - Botni ishga tushirish
/help - Yordam
/admin - Admin panel (faqat admin)

<b>Aloqa:</b>
Muammolar bo'lsa, admin bilan bog'laning.
"""
    await update.message.reply_text(help_text, parse_mode="HTML")


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/admin buyrug'i (faqat admin uchun)"""
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Sizda ruxsat yo'q!")
        return

    stats = get_stats()
    admin_text = f"""
<b>👨‍💼 Admin Panel</b>

<b>📊 Statistika:</b>
👥 Jami foydalanuvchilar: {stats['total_users']}
📱 Bugun faol: {stats['active_today']}
⭐ Jami ballar: {stats['total_points']}
"""

    await update.message.reply_text(
        admin_text,
        parse_mode="HTML",
        reply_markup=get_admin_menu()
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/stats buyrug'i"""
    user_id = update.effective_user.id
    user = get_user(user_id)

    if not user:
        await update.message.reply_text("❌ Avval /start bosing!")
        return

    stats_text = f"""
<b>📊 Sizning statistikangiz:</b>

🏆 Ballar: {user.get('points', 0)}
📚 Tugatilgan darslar: {user.get('lessons_completed', 0)}
📝 Tugatilgan mashqlar: {user.get('exercises_completed', 0)}
📊 Daraja: {user.get('level', 'beginner').upper()}
📅 Qo'shilgan sana: {user.get('joined_date', 'Noma'lum')[:10]}
"""
    await update.message.reply_text(stats_text, parse_mode="HTML")
