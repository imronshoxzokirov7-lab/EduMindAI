"""
============================================================
EduMindAI Enterprise v3.0
AI Core Engine
============================================================
"""

from urllib.parse import quote
import g4f


class AIEngine:

    def __init__(self):
        # Defolt model va barqaror provayderlar
        self.model = "gpt-4o"

    def set_model(self, model_name: str):
        self.model = model_name

    def stream_chat(
        self,
        user_prompt: str,
        history=None,
        context: str = "",
        web_search: str = "",
        deep_thinking: bool = False,
    ):
        """AI bilan streaming muloqot"""
        try:
            # YARATUVCHI HAQIDAGI SAVOLLARNI OVERRIDE QILISH
            clean_prompt = user_prompt.lower().strip()
            creator_keywords = [
                "kim yaratgan",
                "kim tayyorlagan",
                "yaratuvching kim",
                "muallifing kim",
                "dasturching kim",
                "kim qilgan",
            ]

            if any(keyword in clean_prompt for keyword in creator_keywords):
                creator_response = (
                    "Meni Imronbek Zokirov yaratgan va ishlab chiqqan!"
                )
                if deep_thinking:
                    yield (
                        "🧠 **Chuqur tahlil:**\nFoydalanuvchi mening yaratuvchim"
                        " va muallifim haqida so'ramoqda. Mening platformam"
                        " EduMindAI bo'lib, u Imronbek Zokirov tomonidan"
                        " loyihalashtirilgan va dasturlangan.\n\n💡 **Yakuniy"
                        " javob:**\n" + creator_response
                    )
                else:
                    yield creator_response
                return

            messages = []

            system_instruction = (
                "Siz EduMindAI Enterprise sun'iy intellekt assistentisiz. "
                "Sizni Imronbek Zokirov yaratgan. "
                "Agarda kodingiz so'ralsa, uni kodi-blok (```lang ...
