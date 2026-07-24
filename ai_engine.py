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

    # =====================================================

    def get_model(self):

        return self.model

    # =====================================================
    # IMAGE
    # =====================================================

    def image_to_base64(
        self,
        image: Image.Image
    ):

        buffer = io.BytesIO()

        image.convert("RGB").save(
            buffer,
            format="JPEG"
        )

        return base64.b64encode(
            buffer.getvalue()
        ).decode()

    # =====================================================
    # PROMPT
    # =====================================================

    def build_prompt(

        self,

        user_prompt,

        context="",

        web_search=""

    ):

        prompt = self.system_prompt

        if context:

            prompt += "\n\n"

            prompt += "Document Context:\n"

            prompt += context

        if web_search:

            prompt += "\n\n"

            prompt += "Internet Search:\n"

            prompt += web_search

        prompt += "\n\n"

        prompt += f"User:\n{user_prompt}"

        return prompt
        # =====================================================
    # TEXT CHAT
    # =====================================================

    def chat(
        self,
        user_prompt,
        context="",
        web_search=""
    ):

        prompt = self.build_prompt(
            user_prompt,
            context,
            web_search
        )

        try:

            response = self.client.chat.completions.create(

                model=self.model,

                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]

            )

            return response.choices[0].message.content

        except Exception as e:

            return f"❌ AI xatosi:\n\n{str(e)}"

    # =====================================================
    # IMAGE CHAT (VISION)
    # =====================================================

    def vision_chat(
        self,
        image,
        user_prompt,
        context="",
        web_search=""
    ):

        prompt = self.build_prompt(
            user_prompt,
            context,
            web_search
        )

        image64 = self.image_to_base64(image)

        try:

            response = self.client.chat.completions.create(

                model=self.model,

                messages=[

                    {
                        "role": "user",

                        "content": [

                            {
                                "type": "text",

                                "text": prompt
                            },

                            {
                                "type": "image_url",

                                "image_url": {

                                    "url": f"data:image/jpeg;base64,{image64}"

                                }
                            }

                        ]

                    }

                ]

            )

            return response.choices[0].message.content

        except Exception as e:

            return f"❌ Vision xatosi:\n\n{str(e)}"

    # =====================================================
    # AUTO CHAT
    # =====================================================

    def ask(
        self,
        prompt,
        image=None,
        context="",
        web_search=""
    ):

        if image is None:

            return self.chat(
                prompt,
                context,
                web_search
            )

        return self.vision_chat(
            image,
            prompt,
            context,
            web_search
        )
        # =====================================================
    # CONVERSATION MEMORY
    # =====================================================

    def build_messages(
        self,
        user_prompt,
        history=None,
        context="",
        web_search=""
    ):

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        if history:

            for item in history:

                messages.append(
                    {
                        "role": item["role"],
                        "content": item["content"]
                    }
                )

        prompt = self.build_prompt(
            user_prompt,
            context,
            web_search
        )

        messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        return messages

    # =====================================================
    # CHAT WITH MEMORY
    # =====================================================

    def chat_with_memory(
        self,
        user_prompt,
        history=None,
        context="",
        web_search=""
    ):

        messages = self.build_messages(
            user_prompt,
            history,
            context,
            web_search
        )

        try:

            response = self.client.chat.completions.create(

                model=self.model,

                messages=messages

            )

            return response.choices[0].message.content

        except Exception as e:

            return f"❌ {str(e)}"

    # =====================================================
    # STREAM RESPONSE
    # =====================================================

    def stream_chat(
        self,
        user_prompt,
        history=None,
        context="",
        web_search=""
    ):

        messages = self.build_messages(
            user_prompt,
            history,
            context,
            web_search
        )

        try:

            stream = self.client.chat.completions.create(

                model=self.model,

                messages=messages,

                stream=True

            )

            for chunk in stream:

                if hasattr(chunk.choices[0], "delta"):

                    delta = chunk.choices[0].delta

                    if hasattr(delta, "content"):

                        if delta.content:

                            yield delta.content

        except Exception as e:

            yield f"❌ {str(e)}"

    # =====================================================
    # RESET MODEL
    # =====================================================

    def reset(self):

        self.model = DEFAULT_MODEL


# =====================================================
# AI OBJECT
# =====================================================

ai = AIEngine()

