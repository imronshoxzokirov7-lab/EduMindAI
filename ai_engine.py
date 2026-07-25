"""
============================================================
EduMindAI Enterprise v3.0
AI Engine (Pollinations Vision - 100% Free & No API Key Required)
============================================================
"""

import base64
import io
import requests
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
    # VISION CHAT (API KALITSIZ 100% ISHLAYDIGAN VISION)
    # =====================================================

    def vision_chat(self, image: Image.Image, user_prompt: str):
        creator_reply = self._check_creator_question(user_prompt)
        if creator_reply:
            return creator_reply

        try:
            # Rasmni Base64 formatiga o'tkazish
            buffered = io.BytesIO()
            image.convert("RGB").save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            base64_image = f"data:image/jpeg;base64,{img_str}"

            # Pollinations AI ochiq vision serveriga yuborish
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"{user_prompt} (O'zbek tilida batafsil javob ber)"},
                            {"type": "image_url", "image_url": {"url": base64_image}}
                        ]
                    }
                ],
                "model": "openai"
            }

            headers = {"Content-Type": "application/json"}
            response = requests.post("https://text.pollinations.ai/", json=payload, headers=headers, timeout=30)

            if response.status_code == 200:
                return response.text
            else:
                return f"❌ Server javob bermadi (Status Code: {response.status_code})"

        except Exception as e:
            return f"❌ Rasmni tahlil qilishda xatolik yuz berdi: {str(e)}"

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
