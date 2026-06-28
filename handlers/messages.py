"""
Asosiy xabarlar va callback handlerlari
"""
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from utils.database import get_user, update_user, add_points, create_user
from utils.keyboards import (
    get_main_menu, get_levels_menu, get_lessons_menu, 
    get_grammar_topics, get_translation_menu, get_conversation_menu,
    get_exercise_menu, BACK_BUTTON
)
from utils.groq_client import groq

# Foydalanuvchi holatlari (session states)
user_states = {}


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asosiy xabarlarni qayta ishlash"""
    user = update.effective_user
    user_id = user.id
    text = update.message.text

    # Foydalanuvchini tekshirish
    existing_user = get_user(user_id)
    if not existing_user:
        create_user(user_id, user.username, user.first_name)

    # Asosiy menyu tugmalari
    if text == "🇩🇪 Darslar":
        await show_lessons(update, context)
    elif text == "📚 Lug'at":
        await show_vocabulary(update, context)
    elif text == "🔄 Tarjima":
        await show_translation(update, context)
    elif text == "💬 Suhbat":
        await show_conversation(update, context)
    elif text == "📝 Mashq":
        await show_exercises(update, context)
    elif text == "📊 Daraja":
        await show_levels(update, context)
    elif text == "⚙️ Sozlamalar":
        await show_settings(update, context)
    elif text == "❓ Yordam":
        from handlers.commands import help_command
        await help_command(update, context)
    else:
        # Foydalanuvchi holatini tekshirish
        state = user_states.get(user_id, {})
        action = state.get("action")

        if action == "translate_uz_de":
            await do_translation_uz_de(update, context, text)
        elif action == "translate_de_uz":
            await do_translation_de_uz(update, context, text)
        elif action == "conversation":
            await do_conversation(update, context, text)
        elif action == "exercise":
            await do_exercise(update, context, text)
        else:
            # Oddiy suhbat (AI javob)
            await ai_chat(update, context, text)


async def show_lessons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Darslar menyusi"""
    await update.message.reply_text(
        "📚 <b>Darslar bo'limi</b>

"
        "Qaysi turdagi darsni o'rganmoqchisiz?",
        parse_mode="HTML",
        reply_markup=get_lessons_menu()
    )


async def show_vocabulary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lug'at bo'limi"""
    user_id = update.effective_user.id

    # AI orqali kun so'zini olish
    prompt = "Nemis tilida 5 ta foydali so'z va ularning o'zbekcha tarjimasini bering. Format: Nemis - O'zbek - Talaffuz"
    response = groq.chat([
        {"role": "system", "content": "Siz nemis tili o'qituvchisisiz."},
        {"role": "user", "content": prompt}
    ])

    text = f"📚 <b>Kun so'zlari:</b>

{response}

<i>Har kuni yangi so'zlarni o'rganing!</i>"
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=get_main_menu())


async def show_translation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tarjima menyusi"""
    await update.message.reply_text(
        "🔄 <b>Tarjima</b>

"
        "Qaysi yo'nalishda tarjima qilmoqchisiz?",
        parse_mode="HTML",
        reply_markup=get_translation_menu()
    )


async def show_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Suhbat menyusi"""
    await update.message.reply_text(
        "💬 <b>Suhbat mashqi</b>

"
        "Qaysi vaziyatda suhbat qilmoqchisiz?
"
        "AI siz bilan nemis tilida suhbat qiladi.",
        parse_mode="HTML",
        reply_markup=get_conversation_menu()
    )


async def show_exercises(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mashqlar menyusi"""
    await update.message.reply_text(
        "📝 <b>Mashqlar</b>

"
        "Qaysi turdagi mashqni bajarmoqchisiz?",
        parse_mode="HTML",
        reply_markup=get_exercise_menu()
    )


async def show_levels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Darajalar menyusi"""
    await update.message.reply_text(
        "📊 <b>O'z darajangizni tanlang</b>

"
        "Bu darslar va mashqlar sizning darajangizga mos bo'lishi uchun kerak.",
        parse_mode="HTML",
        reply_markup=get_levels_menu()
    )


async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sozlamalar"""
    user = get_user(update.effective_user.id)
    settings = user.get("settings", {})

    notif_status = '✅ Yoqilgan' if settings.get('notifications', True) else '❌ Ochirilgan'
    lang = settings.get('language', 'uz').upper()

    text = (
        "⚙️ <b>Sozlamalar</b>

"
        f"🔔 Bildirishnomalar: {notif_status}
"
        f"🌐 Til: {lang}

"
        "<i>Sozlamalarni o'zgartirish tez orada qo'shiladi.</i>"
    )
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=get_main_menu())


# === TARJIMA FUNKSIYALARI ===

async def do_translation_uz_de(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """O'zbek -> Nemis tarjima"""
    await update.message.reply_text("🔄 Tarjima qilinmoqda...")

    result = groq.translate_to_german(text)

    if result:
        response = f"🇺🇿 <b>Asl matn:</b>
{text}

🇩🇪 <b>Tarjima:</b>
{result}"
        await update.message.reply_text(response, parse_mode="HTML")
        add_points(update.effective_user.id, 1)
    else:
        await update.message.reply_text("❌ Tarjima qilishda xatolik yuz berdi.")

    # Holatni tozalash
    user_states.pop(update.effective_user.id, None)


async def do_translation_de_uz(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """Nemis -> O'zbek tarjima"""
    await update.message.reply_text("🔄 Tarjima qilinmoqda...")

    result = groq.translate_to_uzbek(text)

    if result:
        response = f"🇩🇪 <b>Asl matn:</b>
{text}

🇺🇿 <b>Tarjima:</b>
{result}"
        await update.message.reply_text(response, parse_mode="HTML")
        add_points(update.effective_user.id, 1)
    else:
        await update.message.reply_text("❌ Tarjima qilishda xatolik yuz berdi.")

    user_states.pop(update.effective_user.id, None)


# === SUHBAT FUNKSIYASI ===

async def do_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """Suhbat davomi"""
    user_id = update.effective_user.id
    state = user_states.get(user_id, {})
    scenario = state.get("scenario", "Umumiy suhbat")
    history = state.get("history", [])

    await update.message.reply_text("💭 O'ylayapman...")

    result = groq.practice_conversation(scenario, text, history)

    if result:
        # Tarjima ham qo'shamiz
        translation = groq.translate_to_uzbek(result)

        response = f"🇩🇪 <b>AI:</b>
{result}"
        if translation:
            response += f"

🇺🇿 <b>Tarjima:</b>
{translation}"

        await update.message.reply_text(response, parse_mode="HTML")

        # Tarixni yangilash
        history.append({"role": "user", "content": text})
        history.append({"role": "assistant", "content": result})
        user_states[user_id]["history"] = history[-10:]  # So'nggi 10 ta xabarni saqlash

        add_points(user_id, 2)
    else:
        await update.message.reply_text("❌ Xatolik yuz berdi. Qayta urinib ko'ring.")


# === MASHQ FUNKSIYASI ===

async def do_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """Mashq javobini tekshirish"""
    user_id = update.effective_user.id
    state = user_states.get(user_id, {})
    question = state.get("question", "")
    correct = state.get("correct_answer", "")

    await update.message.reply_text("✅ Tekshirilmoqda...")

    result = groq.check_answer(question, text, correct)

    if result:
        await update.message.reply_text(result, parse_mode="HTML")
        add_points(user_id, 3)
    else:
        await update.message.reply_text("❌ Tekshirishda xatolik.")

    user_states.pop(user_id, None)


# === AI SUHBAT ===

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """Oddiy AI suhbati"""
    user_id = update.effective_user.id

    await update.message.reply_text("🤔 O'ylayapman...")

    messages = [
        {
            "role": "system",
            "content": "Siz nemis tili o'qituvchisisiz. Foydalanuvchi o'zbek tilida savol bersa, o'zbek tilida javob bering. Agar nemis tilida gapirsa, nemis tilida javob bering va xatolarini to'g'rilang. Har doim qisqa va aniq javob bering."
        },
        {"role": "user", "content": text}
    ]

    result = groq.chat(messages)

    if result:
        await update.message.reply_text(result, parse_mode="HTML")
        add_points(user_id, 1)
    else:
        await update.message.reply_text(
            "❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.",
            reply_markup=get_main_menu()
        )
