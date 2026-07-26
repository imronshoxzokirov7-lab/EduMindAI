"""
============================================================
EduMindAI Enterprise v3.0
Data Analyzer Engine (CSV / Excel Tahlili)
============================================================
"""

import pandas as pd
import plotly.express as px
import streamlit as st


class DataAnalyzer:

    @staticmethod
    def read_file(file):
        """Excel yoki CSV faylni pandas DataFrame'ga o'girish"""
        try:
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            return df
        except Exception as e:
            st.error(f"Faylni o'qishda xatolik: {str(e)}")
            return None

    @staticmethod
    def analyze_and_display(df):
        """Jadval va grafikni ekranga chiqarish hamda AI uchun kontekst berish"""
        st.subheader("📊 Fayl Ma'lumotlari Tahlili")

        # 1. Jadval ko'rinishi
        with st.expander("🔍 Jadvalni ko'rish (dastlabki 10 qator)", expanded=True):
            st.dataframe(df.head(10), use_container_width=True)

        # 2. Statistik ma'lumot
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Jami Qatorlar", df.shape[0])
        with col2:
            st.metric("Jami Ustunlar", df.shape[1])

        # 3. Avto-Grafik Yaratish
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

        if num_cols and cat_cols:
            st.markdown("---")
            st.subheader("📈 Avto-Grafik")
            fig = px.bar(df, x=cat_cols[0], y=num_cols[0], title=f"{cat_cols[0]} bo'yicha {num_cols[0]} ko'rsatkichlari")
            st.plotly_chart(fig, use_container_width=True)

        # AI uchun matnli ko'rinish
        summary = f"Faylda {df.shape[0]} ta qator va {df.shape[1]} ta ustun bor. Ustunlar: {', '.join(df.columns)}. Malumotlar namunasi:\n{df.head(5).to_string()}"
        return summary


analyzer = DataAnalyzer()
