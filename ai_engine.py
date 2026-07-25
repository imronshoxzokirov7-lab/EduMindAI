"""
============================================================
EduMindAI Enterprise v3.0
AI Engine (Multi-Fallback Vision Engine - 100% Free)
============================================================
"""

import base64
import io
import requests
from PIL import Image
from g4f.client import Client
from config import DEFAULT_MODEL, SYSTEM_PROMPT


class AIEngine:

    def __init__(self):
        self.client = Client()
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
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )
            for chunk in stream:
                if hasattr(chunk.choices[0], "delta"):
                    delta = chunk.choices[0].delta
                    if hasattr(delta, "content") and delta.content:
                        yield delta.content
        except Exception as e:
            yield f"❌ AI xatosi: {str(e)}"

    # =====================================================
    # VISION CHAT (100% BEPUL VA ISHONCHLI)
    # =====================================================

    def vision_chat(self, image: Image.Image, user_prompt: str):
        creator_reply = self._check_creator_question(user_prompt)
        if creator_reply:
            return creator_reply

        # Rasmni tayyorlash
        img_byte_arr = io.BytesIO()
        image.convert("RGB").save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()

        # 1-USUL: g4f AI Client orqali (gpt-4o vision)
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": f"{user_prompt}\n(Ushbu rasmni diqqat bilan o'rganib chiqib o'zbek tilida javob ber)"}],
                image=img_bytes
            )
            if response and response.choices[0].message.content:
                return response.choices[0].message.content
        except Exception:
            pass

        # 2-USUL: g4f Gemini-flash
        try:
            response = self.client.chat.completions.create(
                model="gemini-flash",
                messages=[{"role": "user", "content": user_prompt}],
                image=img_bytes
            )
            if response and response.choices[0].message.content:
                return response.choices[0].message.content
        except Exception:
            pass

        # 3-USUL: Pollinations AI (Bepul ochiq model bilan)
        try:
            img_str = base64.b64encode(img_bytes).decode("utf-8")
            base64_image = f"data:image/jpeg;base64,{img_str}"

            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"{user_prompt} (O'zbekcha javob ber)"},
                            {"type": "image_url", "image_url": {"url": base64_image}}
                        ]
                    }
                ]
            }
            res = requests.post("https://text.pollinations.ai/", json=payload, headers={"Content-Type": "application/json"}, timeout=25)
            if res.status_code == 200 and len(res.text) > 5:
                return res.text
        except Exception:
            pass

        return "❌ Rasmni tahlil qilishda tarmoq xatoligi yuz berdi. Iltimos, rasmni qayta yuklang va `🗑 Clear Chat` tugmasini bosib ko'ring."

    # =====================================================
    # IMAGE GENERATION
    # =====================================================

    def generate_image(self, prompt: str):
        try:
            response = self.client.images.generate(
                model="flux",
                prompt=prompt,
                response_format="url"
            )
            return response.data[0].url
        except Exception:
            return None


ai = AIEngine()
