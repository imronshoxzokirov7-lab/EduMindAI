"""
============================================================
EduMindAI Enterprise v3.0
Prompt Templates Manager (Tayyor Shablonlar)
============================================================
"""

import streamlit as st


class PromptTemplates:

    TEMPLATES = {
        "📝 Grammatikani tuzatish": "Quyidagi matnning grammatik va imlo xatolarini tuzatib, ravon ko'rinishga keltirib ber:\n\n",
        "🌐 Ingliz tiliga tarjima": "Quyidagi matnni ingliz tiliga professional va tabiy jaranglaydigan tarzda tarjima qilib ber:\n\n",
        "📄 Qisqacha mazmun (Summary)": "Quyidagi matnning eng muhim nuqtalarini ajratib, qisqacha mazmunini punktlar bo'yicha ber:\n\n",
        "💻 Kod xatosini topish (Debug)": "Quyidagi kodni tahlil qil, undagi xatolarni ko'rsat va to'g'rilangan versiyasini tushuntirish bilan ber:\n\n",
        "💡 G'oya yaratish (Brainstorm)": "Quyidagi mavzu bo'yicha 5 ta ijodiy va noyob g'oya taklif qil:\n\n"
    }

    @classmethod
    def render_templates(cls):
        """Yon panelda shablon tugmalarini ko'rsatish"""
        st.subheader("🔤 Quick Prompt Templates")
        selected = st.selectbox("Shablonni tanlang:", list(cls.TEMPLATES.keys()))
        
        if st.button("📌 Shablonni qo'llash", use_container_width=True):
            return cls.TEMPLATES[selected]
        return None


templates = PromptTemplates()
