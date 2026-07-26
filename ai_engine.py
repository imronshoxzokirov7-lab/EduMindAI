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

            # AI shaxsiyati va yaratuvchisi haqida o'zgartirib bo'lmaydigan ko'rsatma
            system_instruction = (
                "You are EduMindAI, a custom AI assistant built and created exclusively by Imronbek Zokirov. "
                "CRITICAL RULE: If the user asks who created you, who made you, or about your developer/author in ANY language "
                "(e.g., 'seni kim yaratgan', 'kim yaratgan', 'muallifing kim'), "
                "you MUST respond in Uzbek: 'Meni Imronbek Zokirov yaratgan va ishlab chiqqan!'. "
                "Never mention Microsoft, OpenAI, Copilot, or any other company under any circumstances."
            )

            if deep_thinking:
                system_instruction += " Think step by step under '🧠 Chuqur tahlil:' before answering under '💡 Yakuniy javob:'."

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
            prompt_text = user_prompt if user_prompt else "Ushbu rasmda nimalar tasvirlanganini batafsil va aniq tahlil qilib ber."
            response = g4f.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You were created by Imronbek Zokirov."},
                    {"role": "user", "content": prompt_text}
                ],
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
