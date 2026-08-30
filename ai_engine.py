"""
============================================================
EduMindAI Enterprise
AI Core Engine
============================================================
"""

import base64
import io

import g4f

try:
    from g4f.client import Client
except ImportError:
    Client = None


class AIEngine:

    def __init__(self):
        self.model = "gpt-3.5-turbo"

        if Client is not None:
            try:
                self.client = Client()
            except Exception:
                self.client = None
        else:
            self.client = None

    # ---------------------------------------------------------
    # MODEL
    # ---------------------------------------------------------

    def set_model(self, model_name: str):
        """AI modelini o'zgartirish."""
        if model_name:
            self.model = model_name

    # ---------------------------------------------------------
    # TEXT CHAT
    # ---------------------------------------------------------

    def stream_chat(
        self,
        user_prompt: str,
        history=None,
        context: str = "",
        web_search: str = "",
        deep_thinking: bool = False,
    ):
        """AI bilan streaming muloqot."""

        try:
            messages = []

            # SYSTEM
            system_instruction = (
                "Siz EduMindAI Enterprise sun'iy intellekt assistentisiz. "
                "Foydalanuvchiga aniq, foydali va tushunarli javob bering. "
                "Kerak bo'lsa kodlarni markdown code block ichida yozing. "
                "Foydalanuvchi qaysi tilda so'rasa, imkon qadar shu tilda javob bering."
            )

            if deep_thinking:
                system_instruction += (
                    " Javob berishdan oldin masalani ichki ravishda "
                    "sinchiklab tekshiring va yakuniy javobni aniq bering."
                )

            messages.append({
                "role": "system",
                "content": system_instruction
            })

            # HISTORY
            if history:
                for message in history:
                    if not isinstance(message, dict):
                        continue

                    role = message.get("role")
                    content = message.get("content")

                    if role in ("user", "assistant") and content:
                        messages.append({
                            "role": role,
                            "content": str(content)
                        })

            # CONTEXT
            extra_context = ""

            if context:
                extra_context += (
                    "\n\n[DOCUMENT / DATA CONTEXT]\n"
                    + str(context)
                )

            if web_search:
                extra_context += (
                    "\n\n[WEB SEARCH CONTEXT]\n"
                    + str(web_search)
                )

            final_prompt = str(user_prompt) + extra_context

            messages.append({
                "role": "user",
                "content": final_prompt
            })

            # -------------------------------------------------
            # G4F CLIENT API
            # -------------------------------------------------

            if self.client is not None:

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=True
                )

                for chunk in response:

                    try:
                        content = chunk.choices[0].delta.content
                    except Exception:
                        content = None

                    if content:
                        yield content

                return

            # -------------------------------------------------
            # OLD G4F API FALLBACK
            # -------------------------------------------------

            response = g4f.ChatCompletion.create(
                model=self.model,
                messages=messages,
                stream=True
            )

            for chunk in response:
                if chunk:
                    yield str(chunk)

        except Exception as e:

            yield (
                "❌ AI bilan bog'lanishda xatolik yuz berdi.\n\n"
                f"Xatolik: `{str(e)}`\n\n"
                "G4F o'rnatilganini va uning versiyasi ishlayotganini "
                "tekshiring."
            )

    # ---------------------------------------------------------
    # NORMAL CHAT
    # ---------------------------------------------------------

    def chat(
        self,
        user_prompt: str,
        history=None,
        context: str = "",
        web_search: str = "",
        deep_thinking: bool = False,
    ):
        """Oddiy, to'liq javob qaytarish."""

        result = ""

        for chunk in self.stream_chat(
            user_prompt=user_prompt,
            history=history,
            context=context,
            web_search=web_search,
            deep_thinking=deep_thinking
        ):
            result += str(chunk)

        return result

    # ---------------------------------------------------------
    # IMAGE GENERATION
    # ---------------------------------------------------------

    def generate_image(
        self,
        prompt: str,
        style: str = "Realistic",
        aspect_ratio: str = "1:1"
    ):
        """AI yordamida rasm yaratish."""

        try:

            if self.client is None:
                return None

            style_instruction = {
                "Realistic": "photorealistic",
                "Anime": "anime style",
                "3D Render": "high quality 3D render",
                "Cyberpunk": "cyberpunk digital art",
                "Oil Painting": "oil painting",
                "Digital Art": "digital art"
            }

            style_text = style_instruction.get(
                style,
                "high quality digital art"
            )

            full_prompt = (
                f"{prompt}. "
                f"Style: {style_text}. "
                f"Aspect ratio: {aspect_ratio}. "
                "High quality, detailed, clean composition."
            )

            response = self.client.images.generate(
                model="flux",
                prompt=full_prompt,
                response_format="url"
            )

            if response and response.data:
                return response.data[0].url

            return None

        except Exception:
            return None

    # ---------------------------------------------------------
    # VISION
    # ---------------------------------------------------------

    def vision_chat(
        self,
        image,
        user_prompt: str
    ):
        """Rasmni AI yordamida tahlil qilish."""

        try:

            if self.client is None:
                return "❌ G4F Client topilmadi."

            # UploadedFile -> bytes
            if hasattr(image, "getvalue"):
                image_bytes = image.getvalue()

            elif hasattr(image, "read"):
                image_bytes = image.read()

            elif isinstance(image, bytes):
                image_bytes = image

            else:
                return "❌ Rasm formatini o'qib bo'lmadi."

            # Base64
            encoded_image = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            # Default MIME
            mime_type = "image/jpeg"

            try:
                file_name = getattr(image, "name", "")

                if file_name.lower().endswith(".png"):
                    mime_type = "image/png"

                elif file_name.lower().endswith(".jpg"):
                    mime_type = "image/jpeg"

                elif file_name.lower().endswith(".jpeg"):
                    mime_type = "image/jpeg"

            except Exception:
                pass

            image_url = (
                f"data:{mime_type};base64,{encoded_image}"
            )

            messages = [
                {
                    "role": "system",
                    "content": (
                        "Siz rasm tahlil qiluvchi AI assistantsiz. "
                        "Rasmni diqqat bilan tahlil qiling va "
                        "foydalanuvchi savoliga aniq javob bering."
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

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )

            try:
                return response.choices[0].message.content
            except Exception:
                return str(response)

        except Exception as e:

            return (
                "❌ Rasmni tahlil qilishda xatolik.\n\n"
                f"Xatolik: `{str(e)}`"
            )


# =============================================================
# GLOBAL AI OBJECT
# =============================================================

ai = AIEngine()
