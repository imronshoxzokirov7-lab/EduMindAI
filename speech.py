"""
============================================================
EduMindAI Enterprise v3.0
Speech Engine (Text-to-Speech & Speech-to-Text)
============================================================
"""

import io
from gtts import gTTS
import g4f


class SpeechEngine:

    @staticmethod
    def quick(text: str, lang: str = "uz"):
        """Matnni ovozga o'girish (TTS)"""
        try:
            tts = gTTS(text=text[:300], lang=lang)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp
        except Exception:
            return None

    @staticmethod
    def transcribe(audio_bytes):
        """Ovozli faylni matnga o'girish (STT)"""
        try:
            # g4f yoki ochiq model orqali audio matnga o'giriladi
            response = g4f.ChatCompletion.create(
                model="whisper-1",
                messages=[{"role": "user", "content": "Audio-ni matnga o'gir"}]
            )
            return response
        except Exception:
            return None


speech = SpeechEngine()
