"""
Telegram inline va reply keyboardlar
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


# Asosiy menyu - AI Chat tugmasi qo'shildi
MAIN_MENU = [
    ["🇩🇪 Darslar", "📚 Lug'at"],
    ["🔄 Tarjima", "💬 Suhbat"],
    ["📝 Mashq", "📊 Daraja"],
    ["🤖 AI Chat", "⚙️ Sozlamalar"],
    ["❓ Yordam"]
]

def get_main_menu():
    return ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)


# AI Chat menyusi
AI_CHAT_MENU = [
    [InlineKeyboardButton("🆕 Yangi suhbat", callback_data="ai_new_chat")],
    [InlineKeyboardButton("🇩🇪 Nemis tilida gaplash", callback_data="ai_german_mode")],
    [InlineKeyboardButton("🇺🇿 O'zbek tilida gaplash", callback_data="ai_uzbek_mode")],
    [InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")],
]

def get_ai_chat_menu():
    return InlineKeyboardMarkup(AI_CHAT_MENU)


# AI Chat davomida stop tugmasi
AI_STOP_MENU = [
    [InlineKeyboardButton("⏹ Suhbatni tugatish", callback_data="ai_stop")],
]

def get_ai_stop_menu():
    return InlineKeyboardMarkup(AI_STOP_MENU)


# Darajalar menyusi
LEVELS_MENU = [
    [InlineKeyboardButton("A1 - Boshlang'ich", callback_data="level_beginner")],
    [InlineKeyboardButton("A2 - Oddiy", callback_data="level_elementary")],
    [InlineKeyboardButton("B1 - O'rta", callback_data="level_intermediate")],
    [InlineKeyboardButton("B2 - Yuqori o'rta", callback_data="level_upper_intermediate")],
    [InlineKeyboardButton("C1 - Yuqori", callback_data="level_advanced")],
]

def get_levels_menu():
    return InlineKeyboardMarkup(LEVELS_MENU)


# Darslar kategoriyasi
LESSONS_MENU = [
    [InlineKeyboardButton("📖 Grammatika", callback_data="lesson_grammar")],
    [InlineKeyboardButton("🗣️ Suhbatlar", callback_data="lesson_conversation")],
    [InlineKeyboardButton("📰 Matnlar", callback_data="lesson_texts")],
    [InlineKeyboardButton("🎧 Tinglash", callback_data="lesson_listening")],
    [InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")],
]

def get_lessons_menu():
    return InlineKeyboardMarkup(LESSONS_MENU)


# Grammatika mavzulari
GRAMMAR_TOPICS = {
    "beginner": [
        "Artikllar (der, die, das)",
        "Ko'plik (Plural)",
        "Shaxsiy olmoshlar (ich, du, er...)",
        "Fe'llar (sein, haben)",
        "Sifatdoshlar (Adjektive)"
    ],
    "elementary": [
        "Zamonlar (Präsens, Perfekt)",
        "Modal fe'llar (können, müssen...)",
        "Prepositionlar",
        "Buyruq shakli (Imperativ)",
        "Solishtirish (Komparativ, Superlativ)"
    ],
    "intermediate": [
        "O'tgan zamon (Präteritum)",
        "Kelasi zamon (Futur)",
        "Passiv",
        "Konjunktiv II",
        "Qo'shma gaplar"
    ]
}

def get_grammar_topics(level="beginner"):
    buttons = []
    for topic in GRAMMAR_TOPICS.get(level, GRAMMAR_TOPICS["beginner"]):
        buttons.append([InlineKeyboardButton(topic, callback_data=f"grammar_{topic}")])
    buttons.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_lessons")])
    return InlineKeyboardMarkup(buttons)


# Tarjima yo'nalishlari
TRANSLATION_MENU = [
    [InlineKeyboardButton("🇺🇿 → 🇩🇪 O'zbek → Nemis", callback_data="trans_uz_de")],
    [InlineKeyboardButton("🇩🇪 → 🇺🇿 Nemis → O'zbek", callback_data="trans_de_uz")],
    [InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")],
]

def get_translation_menu():
    return InlineKeyboardMarkup(TRANSLATION_MENU)


# Suhbat vaziyatlari
CONVERSATION_SCENARIOS = [
    "Salomlashish va tanishish",
    "Do'kon va xarid",
    "Restoranda",
    "Yo'l so'rash",
    "Mehmonxonada",
    "Doktorda",
    "Ish intervyu",
    "Telefon suhbati"
]

def get_conversation_menu():
    buttons = []
    for scenario in CONVERSATION_SCENARIOS:
        buttons.append([InlineKeyboardButton(scenario, callback_data=f"conv_{scenario}")])
    buttons.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(buttons)


# Mashq turlari
EXERCISE_MENU = [
    [InlineKeyboardButton("📝 Tarjima mashqi", callback_data="ex_translate")],
    [InlineKeyboardButton("🔤 So'z yig'ini", callback_data="ex_vocabulary")],
    [InlineKeyboardButton("📋 Grammatika testi", callback_data="ex_grammar")],
    [InlineKeyboardButton("🎧 Tinglash mashqi", callback_data="ex_listening")],
    [InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")],
]

def get_exercise_menu():
    return InlineKeyboardMarkup(EXERCISE_MENU)


# Admin panel
ADMIN_MENU = [
    [InlineKeyboardButton("📊 Statistika", callback_data="admin_stats")],
    [InlineKeyboardButton("📢 Xabar yuborish", callback_data="admin_broadcast")],
    [InlineKeyboardButton("👥 Foydalanuvchilar", callback_data="admin_users")],
]

def get_admin_menu():
    return InlineKeyboardMarkup(ADMIN_MENU)


# Orqaga tugmasi
BACK_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")]
])
