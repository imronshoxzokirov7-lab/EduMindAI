"""
============================================================
EduMindAI Enterprise v3.0
Speech Manager
============================================================
"""

import tempfile
from gtts import gTTS


class SpeechManager:

    def __init__(self):

        self.language = "uz"

    # =====================================================
    # LANGUAGE
    # =====================================================

    def set_language(
        self,
        language
    ):

        self.language = language

    # =====================================================

    def get_language(self):

        return self.language
        # =====================================================
    # TEXT TO SPEECH
    # =====================================================

    def text_to_speech(
        self,
        text
    ):

        if not text:

            return None

        try:

            tts = gTTS(

                text=text,

                lang=self.language,

                slow=False

            )

            temp = tempfile.NamedTemporaryFile(

                delete=False,

                suffix=".mp3"

            )

            tts.save(temp.name)

            return temp.name

        except Exception:

            return None

    # =====================================================
    # QUICK
    # =====================================================

    def quick(
        self,
        text
    ):

        return self.text_to_speech(text)
        # =====================================================
    # CHECK
    # =====================================================

    def is_available(self):

        return True

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.language = "uz"


# =====================================================
# SPEECH OBJECT
# =====================================================

speech = SpeechManager()

