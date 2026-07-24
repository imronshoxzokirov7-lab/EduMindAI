"""
============================================================
EduMindAI Enterprise v3.0
Configuration File
============================================================
"""

from pathlib import Path
import os

# ============================================================
# PROJECT
# ============================================================

APP_NAME = "EduMindAI Enterprise"

APP_VERSION = "3.0"

DEVELOPER = "Imronbek Zokirov"

LANGUAGE = "uz"

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"

LOG_DIR = BASE_DIR / "logs"

ASSETS_DIR = BASE_DIR / "assets"

EXPORT_DIR = BASE_DIR / "exports"

DATABASE_PATH = DATA_DIR / "edumind.db"

# ============================================================
# CREATE DIRECTORIES
# ============================================================

for folder in [

    DATA_DIR,

    LOG_DIR,

    ASSETS_DIR,

    EXPORT_DIR

]:

    folder.mkdir(exist_ok=True)

# ============================================================
# AI SETTINGS
# ============================================================

DEFAULT_MODEL = "gpt-4o"

TEMPERATURE = 0.7

MAX_TOKENS = 4096

SYSTEM_NAME = "EduMindAI"

SYSTEM_PROMPT = """
Siz EduMindAI Enterprise sun'iy intellektisiz.

Asosiy qoidalar:

1. Har doim foydalanuvchiga o'zbek tilida javob bering.
2. Agar foydalanuvchi boshqa tilni so'ramasa, boshqa tilda javob bermang.
3. Javoblaringiz aniq, to'g'ri va tushunarli bo'lsin.
4. Kerak bo'lsa javoblarni punktlar bilan yozing.
5. Dasturlash savollarida faqat ishlaydigan va to'liq kod yozing.
6. Kodlarni izoh bilan tushuntiring.
7. Matematik masalalarni bosqichma-bosqich yeching.
8. Internet ma'lumotlari mavjud bo'lsa, ularni javobga qo'shing.
9. Bilmagan ma'lumotni to'qib chiqarmang, buning o'rniga bu ma'lumot aniq emasligini ayting.
10. Doimo muloyim, professional va foydali yordamchi bo'ling.
"""

# ============================================================
# CHAT SETTINGS
# ============================================================

MAX_CHAT_HISTORY = 100

MAX_MEMORY = 500

ENABLE_WEB_SEARCH = True

ENABLE_TTS = True

ENABLE_VISION = True

ENABLE_EXPORT = True

# ============================================================
# FILE LIMITS
# ============================================================

MAX_IMAGE_SIZE = 10

MAX_FILE_SIZE = 20

ALLOWED_IMAGES = [

    "png",

    "jpg",

    "jpeg"

]

ALLOWED_DOCUMENTS = [

    "pdf",

    "txt",

    "docx",

    "csv",

    "xlsx"

]

# ============================================================
# USER PLANS
# ============================================================

FREE_LIMIT = 25

PRO_LIMIT = 500

ENTERPRISE_LIMIT = -1

FREE_MODEL = "gpt-4o"

PRO_MODEL = "gpt-4o"

ENTERPRISE_MODEL = "gpt-4o"

# ============================================================
# THEME
# ============================================================

DEFAULT_THEME = "light"

PRIMARY_COLOR = "#2D8CFF"

SECONDARY_COLOR = "#121212"

SUCCESS_COLOR = "#00C853"

ERROR_COLOR = "#FF3D00"

WARNING_COLOR = "#FFAB00"

# ============================================================
# SECURITY
# ============================================================

PASSWORD_MIN_LENGTH = 8

SESSION_TIMEOUT = 3600

MAX_LOGIN_ATTEMPTS = 5

# ============================================================
# DATABASE
# ============================================================

DATABASE_TIMEOUT = 30

DATABASE_CACHE = 1000

# ============================================================
# LOGGING
# ============================================================

LOG_FILE = LOG_DIR / "system.log"

LOG_LEVEL = "INFO"

# ============================================================
# EXPORT
# ============================================================

EXPORT_PDF = True

EXPORT_DOCX = True

EXPORT_TXT = True

# ============================================================
# VERSION INFO
# ============================================================

ABOUT = f"""

{APP_NAME}

Version : {APP_VERSION}

Developer : {DEVELOPER}

Enterprise AI Platform

"""
# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

from dotenv import load_dotenv

load_dotenv()

# ============================================================
# API KEYS
# ============================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")

# ============================================================
# AI MODELS
# ============================================================

AVAILABLE_MODELS = {

    "GPT-4o": "gpt-4o",

    "GPT-4.1": "gpt-4.1",

    "GPT-4.1-mini": "gpt-4.1-mini",

    "Gemini 2.5 Flash": "gemini-2.5-flash",

    "Gemini 2.5 Pro": "gemini-2.5-pro",

    "Claude Sonnet": "claude-sonnet-4",

    "DeepSeek Chat": "deepseek-chat",

    "DeepSeek Reasoner": "deepseek-reasoner",

    "Llama 3.3": "llama-3.3",

    "Qwen 3": "qwen3"

}

DEFAULT_MODEL_NAME = "GPT-4o"

# ============================================================
# CHAT LIMITS
# ============================================================

MAX_PROMPT_LENGTH = 15000

MAX_RESPONSE_LENGTH = 8000

MAX_IMAGE_UPLOADS = 10

MAX_DOCUMENT_UPLOADS = 10

MAX_CHAT_EXPORT = 500

# ============================================================
# IMAGE SETTINGS
# ============================================================

IMAGE_WIDTH = 1024

IMAGE_HEIGHT = 1024

IMAGE_QUALITY = 95

# ============================================================
# PDF SETTINGS
# ============================================================

PDF_MAX_PAGES = 500

PDF_MAX_TEXT = 500000

# ============================================================
# AUDIO SETTINGS
# ============================================================

VOICE_LANGUAGE = "uz"

VOICE_SPEED = False

# ============================================================
# CACHE
# ============================================================

CACHE_TIME = 3600

CACHE_SIZE = 500

# ============================================================
# ADMIN
# ============================================================

ADMIN_USERNAME = "admin"

ADMIN_EMAIL = "admin@edumind.ai"

# ============================================================
# DEVELOPER
# ============================================================

CREATOR = "Imronbek Zokirov"

COPYRIGHT = "© EduMindAI Enterprise"

WEBSITE = ""

EMAIL = ""

# ============================================================
# END
# ============================================================

