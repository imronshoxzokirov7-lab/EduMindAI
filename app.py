"""
============================================================
EduMindAI Enterprise v3.5 (Pro Edition)
Main Application
============================================================
"""

import uuid
import streamlit as st
from streamlit_mic_recorder import mic_recorder

from config import *
from database import db
from ai_engine import ai
from search import search
from speech import speech
from vision import vision
from pdf_reader import pdf_reader
from style import style
from export_utils import exporter
from data_analyzer import analyzer
from url_scraper import scraper
from prompt_templates import templates

style.load()

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="EduMindAI Enterprise",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# SESSION STATE & INITIALIZATION
# ==========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "plan" not in st.session_state:
    st.session_state.plan = "Pro Enterprise"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_image" not in st.session_state:
    st.session_state.active_image = None

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "data_summary" not in st.session_state:
    st.session_state.data_summary = ""

if "url_text" not in st.session_state:
    st.session_state.url_text = ""

if "prefilled_prompt" not in st.session_state:
    st.session_state.prefilled_prompt = ""

if "total_prompts" not in st.session_state:
    st.session_state.total_prompts = 0

# ==========================================================
# TITLE & HEADER
# ==========================================================

st.title("🧠 EduMindAI Enterprise v3.5")
st.caption("AI Chat • Multilingual • Code Interpreter • Vision • PDF/Excel • Web Scraper • Deep Reasoning")
st.divider()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:
    st.title("⚙️ EduMindAI Control Center")
    st.markdown("---")

    # 1. ACCOUNT / SIGN IN BO'LIMI
    st.subheader("👤 Account")
    
    if not st.session_state.logged_in:
        st.write("Tizimga kirish uchun email va parolingizni kiriting:")
        email_input = st.text_input("Email:", placeholder="example@gmail.com")
        password_input = st.text_input("Parol:", type="password", placeholder="******")
        
        if st.button("🔑 Sign In", use_container_width=True):
            if email_input and "@" in email_input:
                st.session_state.logged_in = True
                st.session_state.user_email = email_input
                st.success("Muvaffaqiyatli kirdingiz!")
                st.rerun()
            else:
                st.error("Iltimos, to'g'ri email manzilini kiriting!")
    else:
        st.write(f"**Email:** {st.session_state.user_email}")
        st.write(f"**Tarif:** {st.session_state.plan}")
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.rerun()

    st.markdown("---")

    # 2. TIZIM STATISTIKASI (Dashboard Widget)
    st.subheader("📊 Usage Dashboard")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Xabarlar", value=len(st.session_state.messages))
    with col2:
        st.metric(label="So'rovlar", value=st.session_state.total_prompts)

    st.markdown("---")

    # 3. LANGUAGE SELECTION
    st.subheader("🌐 Language Settings")
    app_language = st.selectbox(
        "Muloqot tili (Language):",
        ["O'zbekcha", "English", "Русский"],
        index=0
    )

    st.markdown("---")

    # 4. AI SETTINGS & MODEL SELECTION
    st.subheader("🤖 AI Settings")
    ai_model = st.selectbox("AI Model", ["gpt-4o", "gpt-4.1", "gpt-4", "gpt-3.5-turbo"], index=0)
    ai.set_model(ai_model)

    st.markdown("---")

    # 5. FEATURES & TOGGLES
    st.subheader("⚡ Features")
    enable_web = st.toggle("🌐 Internet Search", value=True)
    enable_memory = st.toggle("🧠 Conversation Memory", value=True)
    enable_tts = st.toggle("🔊 Voice Response", value=False)
    
    voice_gender = "Ayol"
    if enable_tts:
        voice_gender = st.radio("Ovoz turi:", ["Ayol", "Erkak"], horizontal=True)

    enable_img_gen = st.toggle("🎨 Image Generation", value=False)
    enable_deep_think = st.toggle("🔬 Deep Thinking Mode", value=False)

    img_style = "Realistic"
    img_aspect = "1:1"
    if enable_img_gen:
        st.markdown("---")
        st.subheader("🎨 Image Settings")
        img_style = st.selectbox("Uslub (Style):", ["Realistic", "Anime", "3D Render", "Cyberpunk", "Oil Painting", "Digital Art"])
        img_aspect = st.selectbox("O'lcham (Aspect Ratio):", ["1:1", "16:9", "9:16"])

    st.markdown("---")

    # PROMPT TEMPLATES
    template
