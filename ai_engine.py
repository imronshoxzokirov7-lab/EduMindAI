"""
============================================================
EduMindAI Enterprise v3.0
AI Core Engine
============================================================
"""

import g4f


class AIEngine:

    def __init__(self):
        self.model = "gpt-4o"

    def set_model(self, model_name: str):
        self.model = model_name

    def stream_chat(self, user_prompt: str, history=None, context: str = "", web_search: str = "", deep_thinking: bool = False):
        """AI bilan streaming muloqot"""
        try:
            messages = []

            # Kodlarni va umumiy javoblarni tartibli berish bo'yicha kuchaytirilgan ko'rsatma
            system_instruction = (
                "Siz aqlli va yordamchi EduMindAI assistentisiz. "
                "Agarda foydalanuvchi dasturlash kodi so'rasa yoki kod xatosini tuzatishni so'rasa, "
                "kodni albatta tegishli dasturlash tili nomi ko'rsatilgan kodi-blok (```lang ... ```) ichiga oling. "
                "Kodni aniq, toza va bir bosishda nusxalashga qulay qilib taqdim eting."
            )

            if deep_thinking:
                system_instruction += " HAR BIR SAVOLGA JAVOB BERISHDAN OLDIUM '🧠 Chuqur tahlil:' bo'limini ajratib, bosqichma-bosqich mantiqiy o'ylab ko'ring, so'ngra '💡 Yakuniy javob:' qismida aniq javob bering."

            messages.append({"role": "system", "content": system_instruction})

            if context:
                messages.append({"role": "system", "content": f"Qo'shimcha ma'lumotlar:\n{context}"})

            if web_search:
                messages.append({"role": "system", "content": f"Internet qidiruvi:\n{web_search}"})

            if history:
                for msg in history[-6:]:
                    messages.append({"role": msg["role"], "content": msg["content"]})

            messages.append({"role": "user", "content": user_prompt})

            response = g4f.ChatCompletion.create(
                model=self.model,
                messages=messages,
                stream=True
            )

            for chunk in response:
                yield chunk

        except Exception as e:
            yield f"❌ Xatolik yuz berdi: {str(e)}"

    def vision_chat(self, image, user_prompt: str):
        """Rasm tahlili"""
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": user_prompt}],
                image=image
            )
            return response
        except Exception as e:
            return f"❌ Rasm tahlilida xatolik: {str(e)}"

    def generate_image(self, prompt: str, style: str = "Realistic", aspect_ratio: str = "1:1"):
        """Sozlamalar bilan rasm yaratish"""
        try:
            dimensions = {"1:1": (1024, 1024), "16:9": (1280, 720), "9:16": (720, 1280)}
            width, height = dimensions.get(aspect_ratio, (1024, 1024))
            
            full_prompt = f"{prompt}, {style} style, highly detailed, 8k"
            
            return f"https://image.pollinations.ai/prompt/{full_prompt.replace(' ', '%20')}?width={width}&height={height}&nologo=true"
        except Exception:
            return None


ai = AIEngine()
