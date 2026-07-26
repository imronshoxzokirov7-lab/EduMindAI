"""
============================================================
EduMindAI Enterprise v3.0
Speech / TTS Engine (Microsoft Edge Uzbek Voice)
============================================================
"""

import asyncio
import edge_tts


class SpeechEngine:

    @staticmethod
    def quick(text: str, voice: str = "uz-UZ-MadinaNeural"):
        """Matnni O'zbekcha tabiiy ovozga aylantirish"""
        try:
            # Matn juda uzun bo'lsa, tez ishlashi uchun birinchi 300 belgisini o'qiydi
            short_text = text[:300] if len(text) > 300 else text

            async def _generate_audio():
                communicate = edge_tts.Communicate(short_text, voice)
                audio_data = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data += chunk["data"]
                return audio_data

            # Asyncio orqali audio yaratish
            return asyncio.run(_generate_audio())

        except Exception as e:
            return None


speech = SpeechEngine()
