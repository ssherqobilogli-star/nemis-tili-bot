"""
Inline tugmalar (callback) handlerlari
"""
from telegram import Update
from telegram.ext import ContextTypes
from utils.database import update_user, get_user
from utils.keyboards import (
    get_main_menu, get_lessons_menu, get_grammar_topics,
    get_exercise_menu, get_conversation_menu
)
from utils.groq_client import groq
from handlers.messages import user_states


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback querylarni qayta ishlash"""
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = update.effective_user.id

    # === DARAJALAR ===
    if data.startswith("level_"):
        level = data.replace("level_", "")
        level_names = {
            "beginner": "A1 - Boshlang'ich",
            "elementary": "A2 - Oddiy",
            "intermediate": "B1 - O'rta",
            "upper_intermediate": "B2 - Yuqori o'rta",
            "advanced": "C1 - Yuqori"
        }
        update_user(user_id, level=level)
        await query.edit_message_text(
            f"✅ Darajangiz tanlandi: <b>{level_names.get(level, level)}</b>

"
            f"Endi "🇩🇪 Darslar" bo'limidan boshlang!",
            parse_mode="HTML"
        )
        await context.bot.send_message(
            user_id,
            "Asosiy menyu:",
            reply_markup=get_main_menu()
        )

    # === DARSLAR ===
    elif data == "lesson_grammar":
        user = get_user(user_id)
        level = user.get("level", "beginner")
        await query.edit_message_text(
            "📖 <b>Grammatika darslari</b>

"
            "Mavzuni tanlang:",
            parse_mode="HTML",
            reply_markup=get_grammar_topics(level)
        )

    elif data == "lesson_conversation":
        await query.edit_message_text(
            "🗣️ <b>Suhbat darslari</b>

"
            "Tez orada qo'shiladi!",
            parse_mode="HTML"
        )
        await context.bot.send_message(user_id, "Asosiy menyu:", reply_markup=get_main_menu())

    elif data == "lesson_texts":
        await query.edit_message_text(
            "📰 <b>Matnlar</b>

"
            "Tez orada qo'shiladi!",
            parse_mode="HTML"
        )
        await context.bot.send_message(user_id, "Asosiy menyu:", reply_markup=get_main_menu())

    elif data == "lesson_listening":
        await query.edit_message_text(
            "🎧 <b>Tinglash mashqlari</b>

"
            "Tez orada qo'shiladi!",
            parse_mode="HTML"
        )
        await context.bot.send_message(user_id, "Asosiy menyu:", reply_markup=get_main_menu())

    # === GRAMMATIKA MAVZULARI ===
    elif data.startswith("grammar_"):
        topic = data.replace("grammar_", "")
        user = get_user(user_id)
        level = user.get("level", "beginner")

        await query.edit_message_text("📖 Dars tayyorlanmoqda...")

        lesson = groq.generate_lesson(topic, level)

        if lesson:
            # Xabar uzunligini tekshirish (Telegram limit: 4096)
            if len(lesson) > 4000:
                parts = [lesson[i:i+4000] for i in range(0, len(lesson), 4000)]
                await query.edit_message_text(f"📖 <b>{topic}</b>

{parts[0]}", parse_mode="HTML")
                for part in parts[1:]:
                    await context.bot.send_message(user_id, part, parse_mode="HTML")
            else:
                await query.edit_message_text(
                    f"📖 <b>{topic}</b>

{lesson}",
                    parse_mode="HTML"
                )
        else:
            await query.edit_message_text("❌ Dars yaratishda xatolik.")

        await context.bot.send_message(user_id, "Asosiy menyu:", reply_markup=get_main_menu())
        update_user(user_id, lessons_completed=get_user(user_id).get("lessons_completed", 0) + 1)

    # === TARJIMA ===
    elif data == "trans_uz_de":
        user_states[user_id] = {"action": "translate_uz_de"}
        await query.edit_message_text(
            "🇺🇿➡️🇩🇪 <b>O'zbek -> Nemis tarjima</b>

"
            "Tarjima qilmoqchi bo'lgan matningizni yuboring:",
            parse_mode="HTML"
        )

    elif data == "trans_de_uz":
        user_states[user_id] = {"action": "translate_de_uz"}
        await query.edit_message_text(
            "🇩🇪➡️🇺🇿 <b>Nemis -> O'zbek tarjima</b>

"
            "Tarjima qilmoqchi bo'lgan matningizni yuboring:",
            parse_mode="HTML"
        )

    # === SUHBAT ===
    elif data.startswith("conv_"):
        scenario = data.replace("conv_", "")
        user_states[user_id] = {
            "action": "conversation",
            "scenario": scenario,
            "history": []
        }
        await query.edit_message_text(
            f"💬 <b>Suhbat mashqi: {scenario}</b>

"
            f"Nemis tilida gapirishni boshlang!
"
            f"(Agar tugatmoqchi bo'lsangiz, /stop deb yozing)",
            parse_mode="HTML"
        )

    # === MASHQLAR ===
    elif data == "ex_translate":
        user_states[user_id] = {"action": "exercise", "type": "translate"}
        await query.edit_message_text(
            "📝 <b>Tarjima mashqi</b>

"
            "Tez orada qo'shiladi!",
            parse_mode="HTML"
        )
        await context.bot.send_message(user_id, "Asosiy menyu:", reply_markup=get_main_menu())

    elif data == "ex_vocabulary":
        # AI orqali so'z yig'ini mashqi
        await query.edit_message_text("📝 Mashq tayyorlanmoqda...")

        prompt = "Nemis tilida 1 ta so'z va 4 ta variant berib, to'g'ri javobni ko'rsating. Format: So'z: [nemis so'z]
A) variant1 B) variant2 C) variant3 D) variant4
Javob: [harf]"
        exercise = groq.chat([
            {"role": "system", "content": "Siz nemis tili o'qituvchisisiz."},
            {"role": "user", "content": prompt}
        ])

        if exercise:
            await query.edit_message_text(f"📝 <b>So'z yig'ini mashqi:</b>

{exercise}", parse_mode="HTML")
        else:
            await query.edit_message_text("❌ Mashq yaratishda xatolik.")

        await context.bot.send_message(user_id, "Asosiy menyu:", reply_markup=get_main_menu())

    elif data == "ex_grammar":
        user_states[user_id] = {"action": "exercise", "type": "grammar"}
        await query.edit_message_text(
            "📝 <b>Grammatika testi</b>

"
            "Tez orada qo'shiladi!",
            parse_mode="HTML"
        )
        await context.bot.send_message(user_id, "Asosiy menyu:", reply_markup=get_main_menu())

    elif data == "ex_listening":
        await query.edit_message_text(
            "🎧 <b>Tinglash mashqi</b>

"
            "Tez orada qo'shiladi!",
            parse_mode="HTML"
        )
        await context.bot.send_message(user_id, "Asosiy menyu:", reply_markup=get_main_menu())

    # === ORQAGA ===
    elif data == "back_main":
        await query.edit_message_text("Asosiy menyu:")
        await context.bot.send_message(user_id, "Asosiy menyu:", reply_markup=get_main_menu())

    elif data == "back_lessons":
        await query.edit_message_text(
            "📚 <b>Darslar bo'limi</b>",
            parse_mode="HTML",
            reply_markup=get_lessons_menu()
        )


    # === AI CHAT ===
    elif data == "ai_new_chat":
        from handlers.messages import user_states, show_ai_chat
        from utils.keyboards import get_ai_stop_menu
        user_states[user_id] = {"action": "ai_chat", "ai_mode": "auto", "ai_history": []}
        await query.edit_message_text(
            "🤖 <b>AI Chat boshlandi!</b>\n\n"
            "Endi menga istalgan narsani yozing — o\'zbek yoki nemis tilida.\n"
            "Men javob beraman, xatolaringizni to\'g\'rilaman va tushuntiraman.\n\n"
            "<i>Tugatish uchun ⏹ tugmasini bosing</i>",
            parse_mode="HTML",
            reply_markup=get_ai_stop_menu()
        )

    elif data == "ai_german_mode":
        from handlers.messages import user_states
        from utils.keyboards import get_ai_stop_menu
        user_states[user_id] = {"action": "ai_chat", "ai_mode": "german", "ai_history": []}
        await query.edit_message_text(
            "🇩🇪 <b>Nemis tilida suhbat rejimi!</b>\n\n"
            "Men FAQAT nemis tilida javob beraman.\n"
            "Xatolaringizni to\'g\'rilaman va tarjima beraman.\n\n"
            "<i>Guten Start! Schreiben Sie auf Deutsch! ✍️</i>",
            parse_mode="HTML",
            reply_markup=get_ai_stop_menu()
        )

    elif data == "ai_uzbek_mode":
        from handlers.messages import user_states
        from utils.keyboards import get_ai_stop_menu
        user_states[user_id] = {"action": "ai_chat", "ai_mode": "uzbek", "ai_history": []}
        await query.edit_message_text(
            "🇺🇿 <b>O\'zbek tilida suhbat rejimi!</b>\n\n"
            "Nemis tili haqida istalgan savolingizni bering.\n"
            "Men o\'zbek tilida tushuntiraman va misollar keltiraman.\n\n"
            "<i>Savolingizni yozing! 💬</i>",
            parse_mode="HTML",
            reply_markup=get_ai_stop_menu()
        )

    elif data == "ai_stop":
        from handlers.messages import user_states
        user_states.pop(user_id, None)
        await query.edit_message_text(
            "✅ <b>AI Chat tugatildi.</b>\n\nAsosiy menyuga qaytdingiz.",
            parse_mode="HTML"
        )
        await context.bot.send_message(user_id, "Asosiy menyu:", reply_markup=get_main_menu())

    # === ADMIN ===
    elif data == "admin_stats":
        from utils.database import get_stats
        stats = get_stats()
        await query.edit_message_text(
            f"📊 <b>Statistika:</b>

"
            f"👥 Jami foydalanuvchilar: {stats['total_users']}
"
            f"📱 Bugun faol: {stats['active_today']}
"
            f"⭐ Jami ballar: {stats['total_points']}",
            parse_mode="HTML"
        )

    elif data == "admin_broadcast":
        await query.edit_message_text(
            "📢 <b>Xabar yuborish</b>

"
            "Barcha foydalanuvchilarga yuboriladigan xabarni yozing:",
            parse_mode="HTML"
        )
        user_states[user_id] = {"action": "broadcast"}

    elif data == "admin_users":
        from utils.database import get_all_users
        users = get_all_users()
        user_list = "👥 <b>Foydalanuvchilar:</b>

"
        for uid, udata in list(users.items())[:20]:  # Faqat 20 tasi
            user_list += f"• {udata.get('first_name', 'Nomalum')} (@{udata.get('username', 'N/A')})
"
        await query.edit_message_text(user_list, parse_mode="HTML")
