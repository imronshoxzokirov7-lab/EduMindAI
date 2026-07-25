"""
============================================================
EduMindAI Enterprise v3.0
AI Engine
============================================================
"""

import base64
import io
import g4f
from PIL import Image
from config import DEFAULT_MODEL, SYSTEM_PROMPT


class AIEngine:

    def __init__(self):
        self.model = DEFAULT_MODEL
        self.system_prompt = SYSTEM_PROMPT

    def set_model(self, model):
        self.model = model

    def build_prompt(self, user_prompt, context="", web_search=""):
        prompt = self.system_prompt
        if context:
            prompt += f"\n\nDocument Context:\n{context}"
        if web_search:
            prompt += f"\n\nInternet Search:\n{web_search}"
        prompt += f"\n\nUser:\n{user_prompt}"
        return prompt

    def _check_creator_question(self, user_prompt):
        lower_prompt = user_prompt.lower()
        questions = ["kim yaratgan", "muallifing kim", "sizni kim yaratgan", "kimsan", "isming nima", "kim ishlab chiqqan"]
        if any(q in lower_prompt for q in questions):
            return "Meni **Imronbek Zokirov** yaratgan va ishlab chiqqan! Men EduMindAI Enterprise assistentiman."
        return None

    # =====================================================
    # TEXT CHAT
    # =====================================================

    def stream_chat(self, user_prompt, history=None, context="", web_search=""):
        creator_reply = self._check_creator_question(user_prompt)
        if creator_reply:
            yield creator_reply
            return

        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            for item in history:
                messages.append({"role": item["role"], "content": item["content"]})

        prompt = self.build_prompt(user_prompt, context, web_search)
        messages.append({"role": "user", "content": prompt})

        try:
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4o,
                messages=messages,
                stream=True
            )
            for chunk in response:
                yield chunk
        except Exception as e:
            yield f"❌ Xatolik yuz berdi: {str(e)}"

    # =====================================================
    # VISION CHAT (Rasmlarni Tahlil Qilish)
    # =====================================================

    def vision_chat(self, image: Image.Image, user_prompt: str):
        creator_reply = self._check_creator_question(user_prompt)
        if creator_reply:
            return creator_reply

        try:
            # Rasmni JPEG formatida saqlash
            img_byte_arr = io.BytesIO()
            image.convert("RGB").save(img_byte_arr, format='JPEG')
            img_bytes = img_byte_arr.getvalue()

            # g4f gpt-4o vision orqali tahlil qilish
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4o,
                provider=g4f.Provider.Bing,
                messages=[{"role": "user", "content": f"{user_prompt}\n(Ushbu rasmni tahlil qil va savolga javob ber)"}],
                image=img_bytes
            )
            return response
        except Exception:
            try:
                # Muqobil Provayder (Pollinations / Gemini)
                response = g4f.ChatCompletion.create(
                    model="gemini",
                    messages=[{"role": "user", "content": f"{user_prompt}"}],
                    image=img_byte_arr.getvalue()
                )
                return response
            except Exception as e:
                return "❌ Hozirda bepul rasm tahlil serverlarida bandlik yuqori. Birozdan so'ng qayta urinib ko'ring yoki rasmni qayta yuklang."

    # =====================================================
    # IMAGE GENERATION
    # =====================================================

    def generate_image(self, prompt: str):
        try:
            response = g4f.ChatCompletion.create(
                model="flux",
                messages=[{"role": "user", "content": prompt}]
            )
            return response
        except Exception:
            return None


ai = AIEngine()
