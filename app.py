import streamlit as st
import time
import sqlite3
import uuid
from g4f.client import Client
from PIL import Image
from pypdf import PdfReader
from gtts import gTTS
from duckduckgo_search import DDGS

# AI Clientini yaratish
client = Client()

# Sahifa sozlamalari
st.set_page_config(page_title="EduMindAI Enterprise", page_icon="🧠", layout="wide")

# ---------------- MA'LUMOTLAR BAZASI (SQLITE) ----------------
conn = sqlite3.connect("edumind.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                role TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')
conn.commit()

# Har bir foydalanuvchi uchun alohida unikal ID yaratamiz (Aralashib ketmasligi uchun)
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]

USER_KEY = st.session_state.user_id

# ---------------- WEB SEARCH FUNKSIYASI ----------------
def search_web(query):
    try:
        results = DDGS().text(query, max_results=3)
        search_text = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
        return search_text
    except Exception as e:
        return ""

# ---------------- OVOZ YARATISH FUNKSIYASI (TTS) ----------------
def text_to_speech(text, lang='uz'):
    try:
        clean_text = text[:300].replace("*", "").replace("#", "")
        tts = gTTS(text=clean_text, lang='tr' if lang=='uz' else 'en', slow=False)
        filename = "ai_response.mp3"
        tts.save(filename)
        return filename
    except Exception as e:
        return None

# ---------------- MAIN APP ----------------
st.title("🧠 EduMindAI Enterprise")
st.caption("Multimodal AI, Web Search, Audio & Database")

if "messages" not in st.session_state:
    st.session_state.messages = []
    c.execute("SELECT role, content FROM chat_history WHERE username = ? ORDER BY id ASC", (USER_KEY,))
    db_messages = c.fetchall()
    if db_messages:
        for r, c_text in db_messages:
            st.session_state.messages.append({"role": r, "content": c_text, "image": None})
    else:
        st.session_state.messages = [
            {"role": "assistant", "content": "Salom! Men EduMindAI Enterprise assistentiman. Sizga qanday yordam bera olaman?", "image": None}
        ]

if "current_image" not in st.session_state:
    st.session_state.current_image = None
if "extracted_pdf_text" not in st.session_state:
    st.session_state.extracted_pdf_text = ""

# ---------------- CHAP PANEL ----------------
with st.sidebar:
    st.header("⚙️ Funksiyalar va Qidiruv")
    
    use_web_search = st.checkbox("🌐 Internetdan real-vaqtda qidirish", value=False)
    enable_tts = st.checkbox("🔊 AI javobini ovozli o'qish (TTS)", value=True)

    tab1, tab2 = st.tabs(["📄 Fayl/PDF", "🖼️ Rasm"])

    with tab1:
        files = st.file_uploader("PDF/TXT yuklang", type=["pdf", "txt"], accept_multiple_files=True)
        if files:
            for file in files:
                if file.type == "application/pdf":
                    reader = PdfReader(file)
                    text = "".join([page.extract_text() or "" for page in reader.pages])
                    st.session_state.extracted_pdf_text += f"\n--- {file.name} ---\n" + text
                elif file.type == "text/plain":
                    text = str(file.read(), "utf-8")
                    st.session_state.extracted_pdf_text += f"\n--- {file.name} ---\n" + text
            st.success("📄 Fayllar o'qib olindi!")

    with tab2:
        image_file = st.file_uploader("Rasm yuklang", type=["jpg", "png", "jpeg"])
        if image_file:
            st.session_state.current_image = Image.open(image_file)
            st.image(st.session_state.current_image, use_container_width=True)
            st.success("🖼️ Rasm yuklandi!")

    st.markdown("---")
    ai_mode = st.selectbox(
        "AI Rejimini tanlang:",
        ["🎓 O'qituvchi Rejimi (Batafsil)", "⚡ Qisqa va Tezkor", "💻 Dasturchi Rejimi"]
    )

    system_prompts = {
        "🎓 O'qituvchi Rejimi (Batafsil)": "Siz tajribali o'qituvchisiz. Savollarga o'zbek tilida, tushunarli va batafsil javob bering.",
        "⚡ Qisqa va Tezkor": "Siz qisqa va aniq javob beruvchi assistentsiz.",
        "💻 Dasturchi Rejimi": "Siz tajribali dasturchisiz. Kodingizni toza va xatosiz ko'rinishda taqdim eting."
    }

    if st.button("🗑️ Chatni tozalash", use_container_width=True):
        c.execute("DELETE FROM chat_history WHERE username = ?", (USER_KEY,))
        conn.commit()
        st.session_state.messages = [{"role": "assistant", "content": "Chat tarixi tozalandi!", "image": None}]
        st.session_state.current_image = None
        st.session_state.extracted_pdf_text = ""
        st.rerun()

# ---------------- AI JAVOB FUNKSIYASI ----------------
def get_ai_response(user_prompt, img_obj=None, mode_instruction="", context_text="", web_results=""):
    try:
        full_prompt = f"[{mode_instruction}]\n"
        
        if web_results:
            full_prompt += f"\nInternetdan topilgan so'nggi ma'lumotlar:\n{web_results}\n"
            
        if context_text:
            full_prompt += f"\nYuklangan fayllar mazmuni:\n{context_text[:3000]}\n"
            
        full_prompt += f"\nFoydalanuvchi so'rovi: {user_prompt}"

        if img_obj is not None:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": full_prompt}],
                image=img_obj
            )
        else:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": full_prompt}],
            )
        return response.choices[0].message.content
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"

# ---------------- CHAT INTERFEYSI ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("image") is not None:
            st.image(message["image"], width=300)
        st.markdown(message["content"])

if prompt := st.chat_input("EduMindAI Enterprise'ga savol bering..."):
    img_to_send = st.session_state.current_image
    pdf_context = st.session_state.extracted_pdf_text

    st.session_state.messages.append({"role": "user", "content": prompt, "image": img_to_send})
    c.execute("INSERT INTO chat_history (username, role, content) VALUES (?, ?, ?)", 
              (USER_KEY, "user", prompt))
    conn.commit()

    with st.chat_message("user"):
        if img_to_send is not None:
            st.image(img_to_send, width=300)
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        mode_text = system_prompts.get(ai_mode, "")
        
        web_res = ""
        if use_web_search:
            with st.spinner("🌐 Internetdan so'nggi ma'lumotlar qidirilmoqda..."):
                web_res = search_web(prompt)

        with st.spinner("AI javob tayyorlamoqda..."):
            ai_reply = get_ai_response(prompt, img_to_send, mode_text, pdf_context, web_res)

        typed_text = ""
        for char in ai_reply:
            typed_text += char
            message_placeholder.markdown(typed_text + "▌")
            time.sleep(0.002)
            
        message_placeholder.markdown(ai_reply)

        if enable_tts:
            audio_file = text_to_speech(ai_reply)
            if audio_file:
                st.audio(audio_file)

    st.session_state.messages.append({"role": "assistant", "content": ai_reply, "image": None})
    c.execute("INSERT INTO chat_history (username, role, content) VALUES (?, ?, ?)", 
              (USER_KEY, "assistant", ai_reply))
    conn.commit()

    st.session_state.current_image = None
