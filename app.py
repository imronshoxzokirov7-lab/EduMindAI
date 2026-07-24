"""
============================================================
EduMindAI Enterprise v3.0
Main Application
============================================================
"""

# ==========================================================
# IMPORTS
# ==========================================================

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

if "uploaded_image" not in st.session_state:

    st.session_state.uploaded_image = None

if "document_text" not in st.session_state:

    st.session_state.document_text = ""

# ==========================================================
# TITLE
# ==========================================================

st.title("🧠 EduMindAI Enterprise")

st.caption(
    "AI Chat • Vision • PDF • Internet Search • Voice Assistant"
)

st.divider()
# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("⚙️ EduMindAI")

    st.markdown("---")

    st.subheader("👤 Account")

    st.write(
        f"**Username:** {st.session_state.username}"
    )

    st.write(
        f"**Plan:** {st.session_state.plan}"
    )

    st.markdown("---")

    st.subheader("🤖 AI Settings")

    ai_model = st.selectbox(

        "AI Model",

        [

            "gpt-4o",

            "gpt-4.1",

            "gpt-4",

            "gpt-3.5-turbo"

        ],

        index=0

    )

    ai.set_model(ai_model)

    ai_mode = st.selectbox(

        "AI Mode",

        [

            "Teacher",

            "Programmer",

            "Fast",

            "Creative"

        ]

    )

    st.markdown("---")

    st.subheader("🌐 Features")

    enable_web = st.toggle(

        "Internet Search",

        value=False

    )

    enable_tts = st.toggle(

        "Voice Response",

        value=True

    )

    enable_memory = st.toggle(

        "Conversation Memory",

        value=True

    )

    st.markdown("---")

    st.subheader("📄 Upload")

    uploaded_files = st.file_uploader(

        "PDF / TXT",

        type=[

            "pdf",

            "txt"

        ],

        accept_multiple_files=True

    )

    if uploaded_files:

        st.session_state.document_text = (

            pdf_reader.read_multiple(

                uploaded_files

            )

        )

        st.success("Documents loaded.")

    st.markdown("---")

    uploaded_image = st.file_uploader(

        "Image",

        type=[

            "png",

            "jpg",

            "jpeg"

        ]

    )

    if uploaded_image:

        image = vision.open(

            uploaded_image

        )

        st.session_state.uploaded_image = image

        st.image(

            image,

            use_container_width=True

        )

        st.success("Image loaded.")

    st.markdown("---")

    if st.button(

        "🗑 Clear Chat",

        use_container_width=True

    ):

        st.session_state.messages = []

        st.rerun()
        # ==========================================================
# CHAT HISTORY
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message.get("image") is not None:

            st.image(
                message["image"],
                use_container_width=True
            )

        st.markdown(message["content"])

# ==========================================================
# CHAT INPUT
# ==========================================================

prompt = st.chat_input(
    "EduMindAI Enterprise bilan suhbatni boshlang..."
)

if prompt:

    current_image = st.session_state.uploaded_image

    st.session_state.messages.append({

        "role": "user",

        "content": prompt,

        "image": current_image

    })

    with st.chat_message("user"):

        if current_image is not None:

            st.image(
                current_image,
                use_container_width=True
            )

        st.markdown(prompt)

    web_context = ""

    if enable_web:

        with st.spinner(
            "🌐 Internetdan qidirilmoqda..."
        ):

            web_context = search.search_context(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        response = ""

        history = None

        if enable_memory:

            history = st.session_state.messages

        with st.spinner(
            "🤖 EduMindAI javob tayyorlamoqda..."
        ):

            if current_image is None:

                for chunk in ai.stream_chat(

                    user_prompt=prompt,

                    history=history,

                    context=st.session_state.document_text,

                    web_search=web_context

                ):

                    if chunk is not None:
                        response += str(chunk)

                    placeholder.markdown(
                        response + "▌"
                    )

            else:

                response = ai.vision_chat(

                    image=current_image,

                    user_prompt=prompt,

                    context=st.session_state.document_text,

                    web_search=web_context

                )

        placeholder.markdown(response)

        if enable_tts:

            audio = speech.quick(response)

            if audio:

                st.audio(audio)

    st.session_state.messages.append({

        "role": "assistant",

        "content": response,

        "image": None

    })

    st.session_state.uploaded_image = None
    


   
