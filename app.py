import streamlit as st
import time
import sqlite3
import hashlib
from g4f.client import Client
from PIL import Image
from pypdf import PdfReader
from gtts import gTTS

# AI Clientini yaratish
client = Client()

# Sahifa sozlamalari
st.set_page_config(page_title="EduMindAI Pro — Pro Assistent", page_icon="🧠", layout="wide")

# ---------------- MA'LUMOTLAR BAZASI (SQLITE) ----------------
conn = sqlite3.connect("edumind.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                role TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')
conn.commit()

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

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

# ---------------- AUTH / LOGIN TIZIMI ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.title("🧠 EduMindAI Pro — Tizimga kirish")
    
    auth_tab1, auth_tab2 = st.tabs(["🔑 Kirish", "📝 Ro'yxatdan o'tish"])
    
    with auth_tab1:
        username = st.text_input("Foydalanuvchi nomi", key="login_user")
        password = st.text_input("Parol", type="password", key="login_pass")
        if st.button("Kirish", use_container_width=True):
            hashed_pswd = make_hashes(password)
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pswd))
            result = c.fetchone()
            if result:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Xush kelibsiz, {username}!")
                st.rerun()
            else:
                st.error("Foydalanuvchi nomi yoki parol noto'g'ri!")

    with auth_tab2:
        new_user = st.text_input("Yangi foydalanuvchi nomi", key="reg_user")
        new_password = st.text_input("Yangi parol", type="password", key="reg_pass")
        if st.button("Ro'yxatdan o'tish", use_container_width=True):
            try:
                c.execute("INSERT INTO users(username, password) VALUES (?, ?)", (new_user, make_hashes(new_password)))
                conn.commit()
                st.success("Muvaffaqiyatli ro'yxatdan o'tdingiz! Endi kirish bo'limidan kiring.")
            except:
                st.error("Ushbu foydalanuvchi nomi band!")
    st.stop()

# ---------------- TIZIMGA KIRILGANIDAN SO'NG ----------------
st.title(f"🧠 EduMindAI Pro — Assistent ({st.session_state.username})")
st.caption("Multimodal AI, Ovozli javob va SQLite xotira tizimi")

if "messages" not in st.session_state:
    st.session_state.messages = []
    c.execute("SELECT role, content FROM chat_history WHERE username = ? ORDER BY id ASC", (st.session_state.username,))
    db_messages = c.fetchall()
    if db_messages:
        for r, c_text in db_messages:
            st.session_state.messages.append({"role": r, "content": c_text, "image": None})
    else:
        st.session_state.messages = [
            {"role": "assistant", "content": f"Salom {st.session_state.username}! Men EduMindAI Pro assistentiman. Sizga qanday yordam bera olaman?", "image": None}
        ]

if "current_image" not in st.session_state:
    st.session_state.current_image = None
if "extracted_pdf_text" not in st.session_state:
    st.session_state.extracted_pdf_text = ""

# ---------------- CHAP PANEL ----------------
with st.sidebar:
    st.write(f"👤 **Foydalanuvchi:** {st.session_state.username}")
    if st.button("🚪 Tizimdan chiqish", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.header("🗂️ Multimodal Kirish")
    
    tab1, tab2, tab3 = st.tabs(["📄 Fayl/PDF", "🖼️ Rasm", "🔊 Ovoz Sozlamalari"])

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

    with tab3:
        enable_tts = st.checkbox("🔊 AI javobini ovozli o'qish (TTS)", value=True)

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
        c.execute("DELETE FROM chat_history WHERE username = ?", (st.session_state.username,))
        conn.commit()
        st.session_state.messages = [{"role": "assistant", "content": "Chat tarixi tozalandi!", "image": None}]
        st.session_state.current_image = None
        st.session_state.extracted_pdf_text = ""
        st.rerun()

# ---------------- AI JAVOB FUNKSIYASI ----------------
def get_ai_response(user_prompt, img_obj=None, mode_instruction="", context_text=""):
    try:
        full_prompt = f"[{mode_instruction}]\n"
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

if prompt := st.chat_input("EduMindAI Pro'ga savol bering..."):
    img_to_send = st.session_state.current_image
    pdf_context = st.session_state.extracted_pdf_text

    st.session_state.messages.append({"role": "user", "content": prompt, "image": img_to_send})
    c.execute("INSERT INTO chat_history (username, role, content) VALUES (?, ?, ?)", 
              (st.session_state.username, "user", prompt))
    conn.commit()

    with st.chat_message("user"):
        if img_to_send is not None:
            st.image(img_to_send, width=300)
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        mode_text = system_prompts.get(ai_mode, "")
        
        with st.spinner("AI o'ylamoqda va javob tayyorlamoqda..."):
            ai_reply = get_ai_response(prompt, img_to_send, mode_text, pdf_context)

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
              (st.session_state.username, "assistant", ai_reply))
    conn.commit()

    st.session_state.current_image = None
