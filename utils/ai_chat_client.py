"""
AI Chat - Groq API orqali (bepul!)
"""
from utils.groq_client import GroqClient


class AIChatClient:
    def __init__(self):
        self.groq = GroqClient()

    def chat(self, messages: list, mode: str = "uzbek") -> str:
        if mode == "german":
            system = (
                "Siz nemis tili o'qituvchisisiz. "
                "Foydalanuvchi bilan FAQAT nemis tilida gaplashing. "
                "Agar xato qilsa, muloyimlik bilan to'g'rilang. "
                "Javob oxirida qisqacha o'zbekcha tarjima bering: '🇺🇿 Tarjima: ...' formatida."
            )
        elif mode == "uzbek":
            system = (
                "Siz nemis tili bo'yicha yordamchi AI siz. "
                "Foydalanuvchi o'zbek tilida savol beradi, siz o'zbek tilida javob berasiz. "
                "Nemis tili haqida savollar bo'lsa tushuntirib, misollar keltiring."
            )
        else:  # auto
            system = (
                "Siz nemis tili o'qituvchisisiz va universal AI yordamchisiz. "
                "Foydalanuvchi qaysi tilda yozsa, shu tilda javob bering. "
                "Nemis tilida xato bo'lsa to'g'rilang."
            )

        full_messages = [{"role": "system", "content": system}] + messages
        return self.groq.chat(full_messages)


ai_chat = AIChatClient()
