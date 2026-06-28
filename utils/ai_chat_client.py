"""
Claude (Anthropic) AI Chat uchun client
Foydalanuvchi bilan erkin suhbat + nemis tili tahlili
"""
import requests
import json
from config import ANTHROPIC_API_KEY


class AIChatClient:
    def __init__(self):
        self.api_key = ANTHROPIC_API_KEY
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-sonnet-4-6"

    def chat(self, messages: list, mode: str = "uzbek") -> str:
        """
        Claude bilan suhbat

        Args:
            messages: [{"role": "user/assistant", "content": "..."}]
            mode: "uzbek" | "german" | "auto"

        Returns:
            str: AI javobi
        """
        if mode == "german":
            system = (
                "Siz nemis tili o'qituvchisisiz. "
                "Foydalanuvchi bilan FAQAT nemis tilida gaplashing. "
                "Agar xato qilsa, xatoni muloyimlik bilan to'g'rilang va to'g'ri variantni ko'rsating. "
                "Javob oxirida qisqacha o'zbekcha tarjima bering: '🇺🇿 Tarjima: ...' formatida."
            )
        elif mode == "uzbek":
            system = (
                "Siz nemis tili bo'yicha yordamchi AI siz. "
                "Foydalanuvchi o'zbek tilida savol beradi, siz o'zbek tilida javob berasiz. "
                "Nemis tili haqida savol bo'lsa, tushuntirib bering va misollar keltiring. "
                "Har qanday mavzuda gaplashishingiz mumkin, lekin asosiy yo'nalish nemis tili."
            )
        else:  # auto
            system = (
                "Siz nemis tili o'qituvchisisiz va universal AI yordamchisiz. "
                "Foydalanuvchi qaysi tilda yozsa, shu tilda javob bering (o'zbek yoki nemis). "
                "Nemis tilida xato bo'lsa to'g'rilang. O'zbek tilida savol bo'lsa o'zbekcha javob bering. "
                "Har qanday mavzuda yordam bera olasiz."
            )

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "system": system,
            "messages": messages
        }

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            return data["content"][0]["text"]
        except Exception as e:
            print(f"Claude API xatolik: {e}")
            return None

    def analyze_german_text(self, text: str) -> str:
        """Nemis matni tahlili - xatolarni topish va tushuntirish"""
        messages = [
            {
                "role": "user",
                "content": (
                    f"Quyidagi nemis tilidagi matnni tahlil qiling:\n\n\"{text}\"\n\n"
                    "Quyidagilarni ko'rsating:\n"
                    "1. ✅ To'g'ri qismlar\n"
                    "2. ❌ Xatolar (agar bo'lsa) va to'g'ri varianti\n"
                    "3. 🇺🇿 O'zbekcha tarjima\n"
                    "4. 💡 Foydali maslahat\n\n"
                    "O'zbek tilida javob bering."
                )
            }
        ]

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "system": "Siz nemis tili eksperti va o'qituvchisisiz. O'zbek tilida tushuntiring.",
            "messages": messages
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data["content"][0]["text"]
        except Exception as e:
            print(f"Claude API xatolik: {e}")
            return None


ai_chat = AIChatClient()
