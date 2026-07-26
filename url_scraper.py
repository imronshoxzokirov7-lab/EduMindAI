"""
============================================================
EduMindAI Enterprise v3.0
URL Web Scraper (Veb-saytlarni o'qish va tahlil qilish)
============================================================
"""

import requests
from bs4 import BeautifulSoup
import streamlit as st


class URLScraper:

    @staticmethod
    def scrape_url(url: str):
        """Veb-sayt havolasidan matnlarni ajratib olish"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # keraksiz teg xitlarini olib tashlash
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.extract()

                text = soup.get_text(separator=' ', strip=True)
                # Dastlabki 3000 ta belgini olish (AI uchun yetarli)
                clean_text = ' '.join(text.split())[:3000]
                return clean_text
            else:
                st.error(f"Saytga ulanib bo'lmadi (Status Code: {response.status_code})")
                return ""
        except Exception as e:
            st.error(f"URL o'qishda xatolik: {str(e)}")
            return ""


scraper = URLScraper()
