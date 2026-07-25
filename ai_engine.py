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
from config import DEFAULT_MODEL, SYSTEM_PROMPT


class AIEngine:

    def __init__(self):
        self.client = Client()
        self.model = DEFAULT_MODEL
        self.system_prompt = SYSTEM_PROMPT

    def set_model(self, model):
        self.model = model

    def image_to_base64(self, image: Image.Image):
        buffer = io.BytesIO()
        image.convert("RGB").save(buffer, format="JPEG")
        return base64.b64encode(buffer.getvalue()).decode()

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
    # TEXT STREAM CHAT
    # =====================================================

    def stream_chat(self, user_prompt, history=None, context="", web_search=""):
        creator_reply = self._check_creator_question(user_prompt)
        if creator_reply:
            yield creator_reply
            return

        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            for item in history:
                # Rasmli xabarlar xotiraga xatolik bermasligi uchun faqat matn qismini olamiz
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
    # VISION CHAT (RASM TAHLILI)
    # =====================================================

    def vision_chat(self, image: Image.Image, user_prompt: str):
        creator_reply = self._check_creator_question(user_prompt)
        if creator_reply:
            return creator_reply

        try:
            # Rasmni base64 formatiga o'tkazish
            img_b64 = self.image_to_base64(image)
            image_data_url = f"data:image/jpeg;base64,{img_b64}"

            # Openai / g4f vision formatida yuborish
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"Ushbu rasmni diqqat bilan ko'rib chiqib savolga javob ber: {user_prompt}"},
                            {"type": "image_url", "image_url": {"url": image_data_url}}
                        ]
                    }
                ]
            )
            return response.choices[0].message.content
        except Exception:
            try:
                # Zaxira provider
                img_byte_arr = io.BytesIO()
                image.convert("RGB").save(img_byte_arr, format='JPEG')
                
                response = self.client.chat.completions.create(
                    model="gemini-flash",
                    messages=[{"role": "user", "content": user_prompt}],
                    image=img_byte_arr.getvalue()
                )
                return response.choices[0].message.content
            except Exception as err:
                return f"❌ Rasmni tahlil qilib bo'lmadi. Qaytadan yuklab ko'ring: {str(err)}"

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
