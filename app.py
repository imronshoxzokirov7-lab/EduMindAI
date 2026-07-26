"""
============================================================
EduMindAI Enterprise v3.0
Main Application
============================================================
"""

import uuid
import streamlit as st

from config import *
from database import db
from ai_engine import ai
from search import search
from speech import speech
from vision import vision
from pdf_reader import pdf_reader
from style import style
from export_utils import exporter

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

# ==========================================================
# TITLE
# ==========================================================

st.title("🧠 EduMindAI Enterprise")
st.caption("AI Chat • Vision • Image Generation • PDF • Internet Search • Voice Assistant")
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

    st.markdown("---")

    # ======================================================
    # EXPORT CHAT (Yangi integratsiya qilingan qism)
    # ======================================================
    st.subheader("📥 Export Chat")
    if st.session_state.messages:
        # Word formatida yuklab olish
        docx_data = exporter.to_docx(st.session_state.messages)
        st.download_button(
            label="📄 Word (.docx)",
            data=docx_data,
            file_name="edumind_chat.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

        # PDF formatida yuklab olish
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

    st.subheader("📄 Upload Document")
    uploaded_files = st.file_uploader("PDF / TXT", type=["pdf", "txt"], accept_multiple_files=True)
    if uploaded_files:
        st.session_state.document_text = pdf_reader.read_multiple(uploaded_files)
        st.success("Documents loaded.")

    st.markdown("---")

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

prompt = st.chat_input("EduMindAI Enterprise bilan suhbatni boshlang...")

if prompt:
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

        # 1. RASM YARATISH
        if enable_img_gen:
            with st.spinner("🎨 AI rasm chizmoqda..."):
                img_url = ai.generate_image(prompt)
                if img_url:
                    st.image(img_url, caption=f"Yaratilgan rasm: {prompt}", use_container_width=True)
                    response = f"Mana siz so'ragan rasm: {img_url}"
                else:
                    response = "❌ Rasm yaratishda xatolik yuz berdi."
            placeholder.markdown(response)

        # 2. RASM TAHLILI (VISION)
        elif current_img is not None:
            with st.spinner("🖼️ AI rasmni ko'rib tahlil qilmoqda..."):
                response = ai.vision_chat(image=current_img, user_prompt=prompt)
            placeholder.markdown(response)
            st.session_state.active_image = None

        # 3. ODDIY MATNLI CHAT
        else:
            web_context = ""
            if enable_web:
                with st.spinner("🌐 Internetdan qidirilmoqda..."):
                    web_context = search.search_context(prompt)

            with st.spinner("🤖 EduMindAI javob bermoqda..."):
                history = st.session_state.messages if enable_memory else None
                for chunk in ai.stream_chat(
                    user_prompt=prompt,
                    history=history,
                    context=st.session_state.document_text,
                    web_search=web_context
                ):
                    if chunk is not None:
                        response += str(chunk)
                        placeholder.markdown(response + "▌")
            placeholder.markdown(response)

        # OVOZ
        if enable_tts and not enable_img_gen:
            audio = speech.quick(response)
            if audio:
                st.audio(audio)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "image": None
    })
