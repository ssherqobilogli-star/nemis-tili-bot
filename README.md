# 🇩🇪 Nemis Tili AI Bot

O'zbek tilida nemis tilini o'rganish uchun AI yordamchi Telegram bot.

## Xususiyatlari

- 📚 **Darslar** - Grammatika, suhbatlar, matnlar
- 🔄 **Tarjima** - O'zbek ↔ Nemis (AI orqali)
- 💬 **Suhbat** - AI bilan nemis tilida suhbat mashqi
- 📝 **Mashqlar** - Testlar va mashqlar
- 📊 **Daraja** - A1 dan C1 gacha darajalar
- ⭐ **Ballar tizimi** - O'zlashtirishni kuzatish

## Texnologiyalar

- Python 3.11
- python-telegram-bot
- Groq API (Llama 3.1)
- Railway (hosting)

## O'rnatish

1. **Muhit o'zgaruvchilarini sozlash:**
   ```bash
   cp .env.example .env
   # .env faylini tahrirlang
   ```

2. **Kutubxonalarni o'rnatish:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Botni ishga tushirish:**
   ```bash
   python main.py
   ```

## Railway'da joylashtirish

1. GitHub repozitoriyangizni Railway'ga ulang
2. Muhit o'zgaruvchilarini (TELEGRAM_BOT_TOKEN, GROQ_API_KEY, ADMIN_ID) qo'shing
3. Deploy tugmasini bosing!

## Admin buyruqlari

- `/start` - Botni ishga tushirish
- `/help` - Yordam
- `/stats` - O'z statistikangiz
- `/admin` - Admin panel (faqat admin)

## Litsenziya

MIT License
