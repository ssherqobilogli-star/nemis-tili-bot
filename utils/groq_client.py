"""
Groq API bilan ishlash uchun yordamchi modul
"""
import requests
import json
from config import GROQ_API_KEY, GROQ_MODEL


class GroqClient:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.model = GROQ_MODEL
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    def chat(self, messages, temperature=0.7, max_tokens=2000):
        """
        Groq API orqali suhbat

        Args:
            messages: list of dicts with "role" and "content"
            temperature: 0.0 - 1.0 (creativity)
            max_tokens: max response length

        Returns:
            str: AI javobi
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
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
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Groq API xatolik: {e}")
            return None

    def translate_to_german(self, uzbek_text):
        """O'zbek tilidan nemis tiliga tarjima"""
        messages = [
            {
                "role": "system",
                "content": "Siz professional tarjimon. O'zbek tilidan nemis tiliga aniq va to'g'ri tarjima qiling. Faqat tarjima javobini qaytaring, boshqa izoh bermang."
            },
            {
                "role": "user",
                "content": f"Quyidagi matnni nemis tiliga tarjima qiling: {uzbek_text}"
            }
        ]
        return self.chat(messages, temperature=0.3)

    def translate_to_uzbek(self, german_text):
        """Nemis tilidan o'zbek tiliga tarjima"""
        messages = [
            {
                "role": "system",
                "content": "Siz professional tarjimon. Nemis tilidan o'zbek tiliga aniq va to'g'ri tarjima qiling. Faqat tarjima javobini qaytaring, boshqa izoh bermang."
            },
            {
                "role": "user",
                "content": f"Quyidagi matnni o'zbek tiliga tarjima qiling: {german_text}"
            }
        ]
        return self.chat(messages, temperature=0.3)

    def explain_grammar(self, topic, level="beginner"):
        """Grammatika mavzusini tushuntirish"""
        messages = [
            {
                "role": "system",
                "content": f"Siz nemis tili o'qituvchisisiz. {level} darajasida grammatika mavzusini o'zbek tilida tushuntiring. Misollar keltiring va qisqa mashqlar bering."
            },
            {
                "role": "user",
                "content": f"Mavzu: {topic}"
            }
        ]
        return self.chat(messages, temperature=0.7)

    def generate_lesson(self, topic, level="beginner"):
        """Dars yaratish"""
        messages = [
            {
                "role": "system",
                "content": f"Siz nemis tili o'qituvchisisiz. {level} darajasida '{topic}' mavzusida to'liq dars tayyorlang. Dars quyidagi bo'limlardan iborat bo'lsin:
1. Yangi so'zlar (o'zbekcha tarjimasi bilan)
2. Grammatika qoidasi
3. Misollar
4. Mashq
5. Javoblar"
            },
            {
                "role": "user",
                "content": f"Dars mavzusi: {topic}"
            }
        ]
        return self.chat(messages, temperature=0.8, max_tokens=3000)

    def check_answer(self, question, user_answer, correct_answer=None):
        """Foydalanuvchi javobini tekshirish"""
        messages = [
            {
                "role": "system",
                "content": "Siz nemis tili o'qituvchisisiz. Foydalanuvchi javobini tekshiring. Agar to'g'ri bo'lsa, maqtang. Agar xato bo'lsa, xatoni tushuntiring va to'g'ri javobni ko'rsating. O'zbek tilida javob bering."
            },
            {
                "role": "user",
                "content": f"Savol: {question}\nFoydalanuvchi javobi: {user_answer}"
            }
        ]
        if correct_answer:
            messages[1]["content"] += f"\nTo'g'ri javob: {correct_answer}"
        return self.chat(messages, temperature=0.5)

    def practice_conversation(self, scenario, user_message, history=None):
        """Suhbat mashqi"""
        messages = [
            {
                "role": "system",
                "content": f"Siz nemis tili o'qituvchisisiz. Quyidagi vaziyatda suhbat qiling (faqat nemis tilida): {scenario}. Foydalanuvchi xatolarini to'g'rilang va yangi so'zlarni tushuntiring."
            }
        ]

        if history:
            messages.extend(history)

        messages.append({"role": "user", "content": user_message})
        return self.chat(messages, temperature=0.8)


groq = GroqClient()
