"""
============================================================
EduMindAI Enterprise v3.0
Speech / TTS Engine (gTTS)
============================================================
"""

import io
from gtts import gTTS
import streamlit as st


class SpeechEngine:

    @staticmethod
    def quick(text: str, lang: str = "uz"):
        """Matnni ovozga aylantirib, audio bytes qaytarish"""
        try:
            # Agar matn juda uzun bo'lsa, birinchi 300 ta belgisini o'qiydi (tezroq ishlashi uchun)
            short_text = text[:300] if len(text) > 300 else text
            
            # gTTS yordamida audio yaratish
            tts = gTTS(text=short_text, lang=lang, slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.read()
        except Exception as e:
            # O'zbek tili qo'llab-quvvatlanmasa, ingliz tilida sinab ko'radi
            try:
                tts = gTTS(text=short_text, lang="en", slow=False)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                return fp.read()
            except Exception:
                return None


speech = SpeechEngine()
