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
    enable_web = st.toggle("Internet Search", value=False)
    enable_tts = st.toggle("Voice Response", value=False)
    enable_memory = st.toggle("Conversation Memory", value=False)
    enable_img_gen = st.toggle("🎨 Image Generation", value=False)
    enable_deep_think = st.toggle("🧠 Deep Thinking Mode", value=False)

    # 🎨 RASM SOZLAMALARI (YANGI)
    img_style = "Realistic"
    img_aspect = "1:1"
    if enable_img_gen:
        st.markdown("---")
        st.subheader("🎨 Image Settings")
        img_style = st.selectbox("Uslub (Style):", ["Realistic", "Anime", "3D Render", "Cyberpunk", "Oil Painting", "Digital Art"])
        img_aspect = st.selectbox("O'lcham (Aspect Ratio):", ["1:1", "16:9", "9:16"])

    st.markdown("---")

    # 🔤 PROMPT TEMPLATES
    template_prefix = templates.render_templates()
    if template_prefix:
        st.session_state.prefilled_prompt = template_prefix
        st.success("Shablon tanlandi! Endi matningizni chatga yozing.")

    st.markdown("---")

    # 🔗 URL SCRAPER
    st.subheader("🔗 Web Page / Link Analyzer")
    web_url = st.text_input("Veb-sayt havolasini kiriting (https://...)")
    if web_url:
        with st.spinner("🔗 Sayt ma'lumotlari o'qilmoqda..."):
            st.session_state.url_text = scraper.scrape_url(web_url)
            if st.session_state.url_text:
                st.success("Veb-sayt matni muvaffaqiyatli yuklandi!")

    st.markdown("---")

    # 🎙️ VOICE INPUT
    st.subheader("🎙️ Voice Input")
    audio_record = mic_recorder(
        start_prompt="🔴 Ovoz yozishni boshlash",
        stop_prompt="⬛ To'xtatish",
        key='recorder'
    )

    st.markdown("---")

    # 📥 EXPORT CHAT
    st.subheader("📥 Export Chat")
    if st.session_state.messages:
        docx_data = exporter.to_docx(st.session_state.messages)
        st.download_button(
            label="📄 Word (.docx)",
            data=docx_data,
            file_name="edumind_chat.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

        try:
            pdf_data = exporter.to_pdf(st.session_state.messages)
            st.download_button(
                label="📕 PDF (.pdf)",
                data=bytes(pdf_data),
                file_name="edumind_chat.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception:
            pass
    else:
        st.caption("Chatda xabarlar yo'q.")

    st.markdown("---")

    # 📄 DOCUMENT UPLOAD
    st.subheader("📄 Upload Document")
    uploaded_files = st.file_uploader("PDF / TXT", type=["pdf", "txt"], accept_multiple_files=True)
    if uploaded_files:
        st.session_state.document_text = pdf_reader.read_multiple(uploaded_files)
        st.success("Documents loaded.")

    st.markdown("---")

    # 📊 EXCEL / CSV UPLOAD
    st.subheader("📊 Upload Data (Excel/CSV)")
    data_file = st.file_uploader("Excel / CSV fayl", type=["csv", "xlsx", "xls"])
    if data_file:
        df = analyzer.read_file(data_file)
        if df is not None:
            st.session_state.data_summary = analyzer.analyze_and_display(df)

    st.markdown("---")

    # 🖼️ IMAGE UPLOAD
    st.subheader("🖼️ Upload Image")
    uploaded_image_file = st.file_uploader("Image", type=["png", "jpg", "jpeg"], key="img_input")

    if uploaded_image_file is not None:
        st.session_state.active_image = vision.open(uploaded_image_file)
        st.image(st.session_state.active_image, caption="Kiritilgan rasm", use_container_width=True)

    st.markdown("---")

    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.active_image = None
        st.session_state.document_text = ""
        st.session_state.data_summary = ""
        st.session_state.url_text = ""
        st.session_state.prefilled_prompt = ""
        st.rerun()

# ==========================================================
# CHAT HISTORY
# ==========================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("image") is not None:
            st.image(message["image"], use_container_width=True)
        st.markdown(message["content"])

# ==========================================================
# CHAT INPUT & LOGIC
# ==========================================================

text_prompt = st.chat_input("EduMindAI Enterprise bilan suhbatni boshlang...")

prompt = text_prompt
if audio_record and 'bytes' in audio_record:
    st.audio(audio_record['bytes'], format='audio/wav')
    prompt = "Ovozli xabar qabul qilindi. Ushbu xabarga mos javob ber."

if prompt:
    if st.session_state.prefilled_prompt:
        prompt = st.session_state.prefilled_prompt + prompt
        st.session_state.prefilled_prompt = ""

    current_img = st.session_state.active_image

    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "image": current_img
    })

    with st.chat_message("user"):
        if current_img is not None:
            st.image(current_img, use_container_width=True)
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        response = ""

        # 1. RASM YARATISH (SOZLAMALAR BILAN)
        if enable_img_gen:
            with st.spinner("🎨 AI rasm chizmoqda..."):
                img_url = ai.generate_image(prompt, style=img_style, aspect_ratio=img_aspect)
                if img_url:
                    st.image(img_url, caption=f"Yaratilgan rasm ({img_style}, {img_aspect}): {prompt}", use_container_width=True)
                    response = f"Mana siz so'ragan rasm ({img_style} uslubida): {img_url}"
                else:
                    response = "❌ Rasm yaratishda xatolik yuz berdi."
            placeholder.markdown(response)

        # 2. RASM TAHLILI (VISION)
        elif current_img is not None:
            with st.spinner("🖼️ AI rasmni ko'rib tahlil qilmoqda..."):
                response = ai.vision_chat(image=current_img, user_prompt=prompt)
            placeholder.markdown(response)
            st.session_state.active_image = None

        # 3. ODDIY MATNLI / DATA / URL TAHLIL CHATI
        else:
            web_context = ""
            if enable_web:
                with st.spinner("🌐 Internetdan qidirilmoqda..."):
                    web_context = search.search_context(prompt)

            full_context = st.session_state.document_text
            if st.session_state.data_summary:
                full_context += f"\n\n[EXCEL/CSV DATA SUMMARY]:\n{st.session_state.data_summary}"
            if st.session_state.url_text:
                full_context += f"\n\n[WEBPAGE URL CONTENT]:\n{st.session_state.url_text}"

            with st.spinner("🤖 EduMindAI javob bermoqda..."):
                history = st.session_state.messages if enable_memory else None
                for chunk in ai.stream_chat(
                    user_prompt=prompt,
                    history=history,
                    context=full_context,
                    web_search=web_context,
                    deep_thinking=enable_deep_think
                ):
                    if chunk is not None:
                        response += str(chunk)
                        placeholder.markdown(response + "▌")
            placeholder.markdown(response)

        # OVOZLI JAVOB (TTS)
        if enable_tts and not enable_img_gen:
            audio = speech.quick(response)
            if audio:
                st.audio(audio)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "image": None
    })
