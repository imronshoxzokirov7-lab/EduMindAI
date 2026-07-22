import streamlit as st
import time
from g4f.client import Client
from PIL import Image
from pypdf import PdfReader

# AI Clientini yaratish
client = Client()

# Sahifa sozlamalari
st.set_page_config(page_title="EduMindAI Assistent", page_icon="🧠", layout="wide")

st.title("🧠 EduMindAI — Multimodal AI System")
st.caption("Istalgan savolga real-vaqt rejimida javob beruvchi va multimediani tahlil qiluvchi AI")

# --- SESSION STATE (XOTIRA) SOZLAMALARI ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Salom! Men EduMindAI assistentiman. Menga dunyodagi istalgan savolingizni bering yoki fayl/rasm yuklang!", "image": None}
    ]

if "current_image" not in st.session_state:
    st.session_state.current_image = None

if "extracted_pdf_text" not in st.session_state:
    st.session_state.extracted_pdf_text = ""

# ---------------- CHAP PANEL: MULTIMODAL YUKLASH VA SOZLAMALAR ----------------
with st.sidebar:
    st.header("🗂️ Multimodal Kirish")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Fayl/PDF", "🎙️ Ovoz", "🎥 Video", "🖼️ Rasm"])

    with tab1:
        files = st.file_uploader("Fayllar (PDF, TXT) yuklang", type=["pdf", "txt"], accept_multiple_files=True)
        if files:
            st.success(f"📁 {len(files)} ta fayl qabul qilindi!")
            for file in files:
                if file.type == "application/pdf":
                    reader = PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() or ""
                    st.session_state.extracted_pdf_text += f"\n--- {file.name} ---\n" + text
                    st.info(f"📄 {file.name} matni o'qib olindi!")
                elif file.type == "text/plain":
                    text = str(file.read(), "utf-8")
                    st.session_state.extracted_pdf_text += f"\n--- {file.name} ---\n" + text

    with tab2:
        audio_file = st.file_uploader("Ovozli xabar", type=["mp3", "wav", "m4a"])
        if audio_file:
            st.audio(audio_file)
            st.success("🎙️ Ovozli xabar qabul qilindi!")

    with tab3:
        video_file = st.file_uploader("Video fayl", type=["mp4", "avi", "mov"])
        if video_file:
            st.video(video_file)
            st.success("🎥 Video qabul qilindi!")

    with tab4:
        image_file = st.file_uploader("Rasm yuklang", type=["jpg", "png", "jpeg"])
        if image_file:
            st.session_state.current_image = Image.open(image_file)
            st.image(st.session_state.current_image, use_container_width=True)
            st.success("🖼️ Rasm yuklandi! Endi chatga savolingizni yozing.")

    st.markdown("---")
    st.header("⚙️ AI Sozlamalari")

    ai_mode = st.selectbox(
        "AI Rejimini tanlang:",
        ["🎓 O'qituvchi Rejimi (Batafsil)", "⚡ Qisqa va Tezkor", "💻 Dasturchi Rejimi"]
    )

    system_prompts = {
        "🎓 O'qituvchi Rejimi (Batafsil)": "Siz tajribali o'qituvchisiz. Savollarga o'zbek tilida, tushunarli, misollar bilan va batafsil javob bering.",
        "⚡ Qisqa va Tezkor": "Siz qisqa va aniq javob beruvchi assistentsiz. Ortiqcha gaplarsiz, faqat eng muhim javobni bering.",
        "💻 Dasturchi Rejimi": "Siz tajribali dasturchisiz. Kodingizni tushuntirishlar bilan, toza va xatosiz ko'rinishda taqdim eting."
    }

    if st.button("🗑️ Chatni tozalash", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat tozalandi! Yangi savolingizni berishingiz mumkin.", "image": None}
        ]
        st.session
