import streamlit as st
from openai import OpenAI


class AIEngine:

    def __init__(self):
        self.model = "gpt-4o"

        try:
            api_key = st.secrets["OPENAI_API_KEY"]
            self.client = OpenAI(api_key=api_key)
        except Exception:
            self.client = None

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
        if self.client is None:
            yield "❌ OPENAI_API_KEY topilmadi. Streamlit Secrets bo‘limini tekshiring."
            return

        system_prompt = """
Siz EduMindAI Enterprise sun'iy intellekt assistentisiz.
Foydalanuvchiga aniq, foydali va tushunarli javob bering.
Foydalanuvchi qaysi tilda yozsa, shu tilda javob bering.
Kod so‘ralsa, kodni markdown code block ichida yozing.
"""

        if deep_thinking:
            system_prompt += """
Masalani diqqat bilan tahlil qiling va yakuniy javobni
aniq va tushunarli qilib bering.
"""

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        if history:
            for message in history:
                if message.get("role") in ["user", "assistant"]:
                    content = message.get("content", "")

                    if content:
                        messages.append({
                            "role": message["role"],
                            "content": str(content)
                        })

        if context:
            user_prompt += (
                "\n\nQo‘shimcha hujjat/data:\n"
                + str(context)
            )

        if web_search:
            user_prompt += (
                "\n\nInternet qidiruv natijalari:\n"
                + str(web_search)
            )

        messages.append({
            "role": "user",
            "content": user_prompt
        })

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )

            for chunk in response:
                if chunk.choices:
                    content = chunk.choices[0].delta.content

                    if content:
                        yield content

        except Exception as e:
            yield f"❌ OpenAI xatosi: {str(e)}"

    def chat(
        self,
        user_prompt: str,
        history=None,
        context: str = "",
        web_search: str = "",
        deep_thinking: bool = False,
    ):
        answer = ""

        for chunk in self.stream_chat(
            user_prompt=user_prompt,
            history=history,
            context=context,
            web_search=web_search,
            deep_thinking=deep_thinking
        ):
            answer += str(chunk)

        return answer

    def generate_image(
        self,
        prompt: str,
        style: str = "Realistic",
        aspect_ratio: str = "1:1"
    ):
        if self.client is None:
            return None

        try:
            full_prompt = (
                f"{prompt}. "
                f"Style: {style}. "
                f"Aspect ratio: {aspect_ratio}. "
                "High quality, detailed."
            )

            result = self.client.images.generate(
                model="gpt-image-1",
                prompt=full_prompt,
                size="1024x1024"
            )

            if result.data:
                image_data = result.data[0].b64_json

                if image_data:
                    return f"data:image/png;base64,{image_data}"

            return None

        except Exception:
            return None

    def vision_chat(self, image, user_prompt: str):

        if self.client is None:
            return "❌ OPENAI_API_KEY topilmadi."

        try:
            if hasattr(image, "getvalue"):
                image_bytes = image.getvalue()
            else:
                image_bytes = image.read()

            import base64

            encoded = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            image_url = (
                "data:image/jpeg;base64,"
                + encoded
            )

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Siz rasmni tahlil qiluvchi AI "
                            "assistentisiz."
                        )
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": user_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url
                                }
                            }
                        ]
                    }
                ]
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"❌ Rasmni tahlil qilishda xatolik: {str(e)}"


ai = AIEngine()
