"""
============================================================
EduMindAI Enterprise v3.0
AI Engine
============================================================
"""

import base64
import io
from PIL import Image
from g4f.client import Client
from config import (
    DEFAULT_MODEL,
    SYSTEM_PROMPT
)


class AIEngine:

    def __init__(self):
        self.client = Client()
        self.model = DEFAULT_MODEL
        self.system_prompt = SYSTEM_PROMPT

    # =====================================================
    # MODEL
    # =====================================================

    def set_model(self, model):
        self.model = model

    def get_model(self):
        return self.model

    # =====================================================
    # IMAGE UTILS
    # =====================================================

    def image_to_base64(self, image: Image.Image):
        buffer = io.BytesIO()
        image.convert("RGB").save(buffer, format="JPEG")
        return base64.b64encode(buffer.getvalue()).decode()

    # =====================================================
    # PROMPT BUILDER
    # =====================================================

    def build_prompt(self, user_prompt, context="", web_search=""):
        prompt = self.system_prompt

        if context:
            prompt += f"\n\nDocument Context:\n{context}"

        if web_search:
            prompt += f"\n\nInternet Search:\n{web_search}"

        prompt += f"\n\nUser:\n{user_prompt}"
        return prompt

    def build_messages(self, user_prompt, history=None, context="", web_search=""):
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        if history:
            for item in history:
                messages.append({
                    "role": item["role"],
                    "content": item["content"]
                })

        prompt = self.build_prompt(user_prompt, context, web_search)
        messages.append({
            "role": "user",
            "content": prompt
        })

        return messages

    # =====================================================
    # CREATOR FILTER (Muallifni Himoyalash)
    # =====================================================

    def _check_creator_question(self, user_prompt):
        lower_prompt = user_prompt.lower()
        questions = ["kim yaratgan", "muallifing kim", "sizni kim yaratgan", "kimsan", "isming nima", "kim ishlab chiqqan"]
        if any(q in lower_prompt for q in questions):
            return "Meni **Imronbek Zokirov** yaratgan va ishlab chiqqan! Men EduMindAI Enterprise assistentiman."
        return None

    # =====================================================
    # TEXT CHAT
    # =====================================================

    def chat(self, user_prompt, context="", web_search=""):
        creator_reply = self._check_creator_question(user_prompt)
        if creator_reply:
            return creator_reply

        prompt = self.build_prompt(user_prompt, context, web_search)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ AI xatosi:\n\n{str(e)}"

    # =====================================================
    # STREAM CHAT (Oqimli Javob)
    # =====================================================

    def stream_chat(self, user_prompt, history=None, context="", web_search=""):
        creator_reply = self._check_creator_question(user_prompt)
        if creator_reply:
            yield creator_reply
            return

        messages = self.build_messages(user_prompt, history, context, web_search)

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
            yield f"❌ {str(e)}"

    # =====================================================
    # VISION CHAT (Rasm Tahlili)
    # =====================================================

    def vision_chat(self, image, user_prompt, context="", web_search=""):
        creator_reply = self._check_creator_question(user_prompt)
        if creator_reply:
            return creator_reply

        prompt = self.build_prompt(user_prompt, context, web_search)
        image64 = self.image_to_base64(image)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{image64}"}
                            }
                        ]
                    }
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Vision xatosi:\n\n{str(e)}"

    # =====================================================
    # IMAGE GENERATION (Rasm Yaratish)
    # =====================================================

    def generate_image(self, prompt: str):
        """
        Matnli tasvir orqali AI yordamida rasm yaratish.
        """
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                response_format="url"
            )
            return response.data[0].url
        except Exception:
            try:
                # Muqobil bepul model
                response = self.client.images.generate(
                    model="flux",
                    prompt=prompt,
                    response_format="url"
                )
                return response.data[0].url
            except Exception:
                return None

    # =====================================================
    # AUTO CHAT
    # =====================================================

    def ask(self, prompt, image=None, context="", web_search=""):
        if image is None:
            return self.chat(prompt, context, web_search)
        return self.vision_chat(image, prompt, context, web_search)

    # =====================================================
    # RESET MODEL
    # =====================================================

    def reset(self):
        self.model = DEFAULT_MODEL


# =====================================================
# SINGLETON INSTANCE
# =====================================================

ai = AIEngine()
