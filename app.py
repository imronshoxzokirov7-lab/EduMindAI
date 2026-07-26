"""
============================================================
EduMindAI Enterprise v3.0
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
# SESSION STATE
# ==========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "username" not in st.session_state:
    st.session_state.username = "Guest"

if "plan" not in st.session_state:
    st.session_state.plan = "Free"

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

# ==========================================================
# TITLE
# ==========================================================

st.title("🧠 EduMindAI Enterprise")
st.caption("AI Chat • Vision • Image Generation • PDF • Excel/CSV • Web Scraper • Deep Reasoning • Voice Assistant")
st.divider()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:
    st.title("⚙️ EduMindAI")
    st.markdown("---")

    st.subheader("👤 Account")
    st.write(f"**Username:** {st.session_state.username}")
    st.write(f"**Plan:** {st.session_state.plan}")

    st.markdown("---")

    st.subheader("🤖 AI Settings")
    ai_model = st.selectbox("AI Model", ["gpt-4o", "gpt-4.1", "gpt-4", "gpt-3.5-turbo"], index=0)
    ai.set_model(ai_model)

    st.markdown("---")

    st.subheader("🌐 Features")
    enable_web = st.toggle("Internet Search", value=True)
    enable_tts = st.toggle("Voice Response", value=False)
    enable_memory = st.toggle("Conversation Memory", value=True)
    enable_img_gen = st.toggle("🎨 Image Generation", value=False)
    enable_deep_think = st.toggle("🧠 Deep Thinking Mode", value=False)

    img_style = "Realistic"
    img_aspect = "1:1"
    if enable_img_gen:
        st.markdown("---")
        st.subheader("🎨 Image Settings")
        img_style = st.selectbox("Uslub (Style):", ["Realistic", "Anime", "3D Render", "Cyberpunk", "Oil Painting", "Digital Art"])
        img_aspect = st.selectbox("O'lcham (Aspect Ratio):", ["1:1", "16:9", "9:16"])

    st.markdown("---")

    template_prefix = templates.render_templates()
    if template_prefix:
        st.session_state.
