import streamlit as st
import time
from g4f.client import Client
from PIL import Image

# AI Clientini yaratish
client = Client()

# Sahifa sozlamalari
st.set_page_config(page_title="EduMindAI Assistent", page_icon="🧠", layout="wide")

st.title("🧠 EduMindAI — Multimodal AI System")
st.caption("Istalgan savolga real-vaqt rejimida javob beruvchi va multimediani tahlil qiluvchi AI")

# --- SESSION STATE (XOTIRA) SOZLAMALARI ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Salom! Men EduMindAI assistentiman. Menga dunyodagi istalgan savolingizni bering!", "image": None}
    ]

if "current_image" not in st.session_state:
    st.session_state.current_image = None

# ---------------- CHAP PANEL: MULTIMODAL YUKLASH VA SOZLAMALAR ----------------
with st.sidebar:
    st.header("🗂️ Multimodal Kirish")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Fayl/Papka", "🎙️ Ovoz", "🎥 Video", "🖼️ Rasm"])
    
    uploaded_info = []

    with tab1:
        files = st.file_uploader("Fayllar yoki Papka yuklang", accept_multiple_files=True)
        if files:
            st.success(f"📁 {len(files)} ta fayl qabul qilindi!")
            uploaded_info.append(f"{len(files)} ta fayl")
            for file in files:
                if file.type.startswith("image/"):
                    st.session_state.current_image = Image.open(file)

    with tab2:
        audio_file = st.file_uploader("Ovozli xabar", type=["mp3", "wav", "m4a"])
        if audio_file:
            st.audio(audio_file)
            st.success("🎙️ Ovozli xabar yuklandi!")
            uploaded_info.append("Ovozli xabar")

    with tab3:
        video_file = st.file_uploader("Video fayl", type=["mp4", "avi", "mov"])
        if video_file:
            st.video(video_file)
            st.success("🎥 Video qabul qilindi!")
            uploaded_info.append("Video fayl")

    with tab4:
        image_file = st.file_uploader("Rasm yuklang", type=["jpg", "png", "jpeg"])
        if image_file:
            st.session_state.current_image = Image.open(image_file)
            st.image(st.session_state.current_image, use_container_width=True)
            st.success("🖼️ Rasm yuklandi!")
            uploaded_info.append("Rasm")

    st.markdown("---")
    st.header("⚙️ AI Sozlamalari")

    # 1. AI Rejimini tanlash
    ai_mode = st.selectbox(
        "AI Rejimini tanlang:",
        ["🎓 O'qituvchi Rejimi (Batafsil)", "⚡ Qisqa va Tezkor", "💻 Dasturchi Rejimi"]
    )

    # Rejimga qarab Prompt shakllantirish (Nomlar selectbox bilan bir xil qilindi)
    system_prompts = {
        "🎓 O'qituvchi Rejimi (Batafsil)": "Siz tajribali o'qituvchisiz. Savollarga o'zbek tilida, tushunarli, misollar bilan va batafsil javob bering.",
        "⚡ Qisqa va Tezkor": "Siz qisqa va aniq javob beruvchi assistentsiz. Ortiqcha gaplarsiz, faqat eng muhim javobni bering.",
        "💻 Dasturchi Rejimi": "Siz tajribali dasturchisiz. Kodingizni tushuntirishlar bilan, toza va xatosiz ko'rinishda taqdim eting."
    }

    # 2. Chatni tozalash tugmasi
    if st.button("🗑️ Chatni tozalash", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat tozalandi! Yangi savolingizni berishingiz mumkin.", "image": None}
        ]
        st.session_state.current_image = None
        st.rerun()

    # 3. Chatni yuklab olish (.txt formatda)
    chat_text = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
    st.download_button(
        label="📥 Chatni yuklab olish (.txt)",
        data=chat_text,
        file_name="EduMindAI_Suhbat.txt",
        mime="text/plain",
        use_container_width=True
    )

# ---------------- REAL AI JAVOB BERISH FUNKSIYASI ----------------
def get_ai_response(user_prompt, media_list, img_obj=None, mode_instruction=""):
    try:
        full_prompt = f"[{mode_instruction}]\n\nFoydalanuvchi so'rovi: {user_prompt}"

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
        return f"**EduMindAI Natijasi:**\n\nSizning *'{user_prompt}'* bo'yicha so'rovingiz tahlil qilindi. (Xatolik yuz berdi: {str(e)})"

# ---------------- CHAT INTERFEYSI ----------------
# Tarixdagi xabarlarni chiqarish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("image") is not None:
            st.image(message["image"], width=300)
        st.markdown(message["content"])

# Yangi xabar kelganda
if prompt := st.chat_input("EduMindAI'ga savol bering..."):
    img_to_send = st.session_state.current_image

    # Foydalanuvchi xabarini saqlash
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt, 
        "image": img_to_send
    })
    
    with st.chat_message("user"):
        if img_to_send is not None:
            st.image(img_to_send, width=300)
        st.markdown(prompt)

    # AI javobini olish
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        mode_text = system_prompts.get(ai_mode, "")
        ai_reply = get_ai_response(prompt, uploaded_info, img_to_send, mode_text)

        typed_text = ""
        for char in ai_reply:
            typed_text += char
            message_placeholder.markdown(typed_text + "▌")
            time.sleep(0.005)
            
        message_placeholder.markdown(ai_reply)

    # AI javobini saqlash
    st.session_state.messages.append({
        "role": "assistant", 
        "content": ai_reply, 
        "image": None
    })

    # Rasm yuborilgach xotirani tozalash
    st.session_state.current_image = None
    