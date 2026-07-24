"""
============================================================
EduMindAI Enterprise v3.0
Database Manager
============================================================
"""

import sqlite3
from pathlib import Path
from contextlib import closing

from config import DATABASE_PATH


class Database:
    def __init__(self):
        # Database papkasini yaratish
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

        # SQLite ulanish
        self.conn = sqlite3.connect(
            DATABASE_PATH,
            check_same_thread=False
        )

        self.conn.row_factory = sqlite3.Row

        # Jadvallarni yaratish
        self.create_tables()

    # =====================================================
    # DATABASE HELPERS
    # =====================================================

    def execute(self, query, params=()):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(query, params)
            self.conn.commit()

    def fetchone(self, query, params=()):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def fetchall(self, query, params=()):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    # =====================================================
    # CREATE TABLES
    # =====================================================

    def create_tables(self):
        self.create_users_table()
        self.create_chat_table()
        self.create_memory_table()
        self.create_settings_table()
        self.create_favorites_table()
        self.create_statistics_table()

    # =====================================================
    # USERS
    # =====================================================

    def create_users_table(self):
        self.execute("""
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id TEXT UNIQUE NOT NULL,

            username TEXT UNIQUE NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            plan TEXT DEFAULT 'Free',

            avatar TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

    # =====================================================
    # CHAT HISTORY
    # =====================================================

    def create_chat_table(self):
        self.execute("""
        CREATE TABLE IF NOT EXISTS chat_history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id TEXT NOT NULL,

            role TEXT NOT NULL,

            content TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

    # =====================================================
    # MEMORY
    # =====================================================

    def create_memory_table(self):
        self.execute("""
        CREATE TABLE IF NOT EXISTS memory(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id TEXT NOT NULL,

            title TEXT,

            content TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

    # =====================================================
    # SETTINGS
    # =====================================================

    def create_settings_table(self):
        self.execute("""
        CREATE TABLE IF NOT EXISTS settings(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id TEXT UNIQUE,

            theme TEXT DEFAULT 'light',

            language TEXT DEFAULT 'uz',

            tts INTEGER DEFAULT 1,

            web_search INTEGER DEFAULT 0

        )
        """)

    # =====================================================
    # FAVORITES
    # =====================================================

    def create_favorites_table(self):
        self.execute("""
        CREATE TABLE IF NOT EXISTS favorites(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id TEXT,

            question TEXT,

            answer TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

    # =====================================================
    # STATISTICS
    # =====================================================

    def create_statistics_table(self):
        self.execute("""
        CREATE TABLE IF NOT EXISTS statistics(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id TEXT UNIQUE,

            questions INTEGER DEFAULT 0,

            pdfs INTEGER DEFAULT 0,

            images INTEGER DEFAULT 0,

            voices INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)
            # =====================================================
    # USER FUNCTIONS
    # =====================================================

    def create_user(
        self,
        user_id,
        username,
        email,
        password,
        plan="Free"
    ):

        self.execute(
            """
            INSERT INTO users(
                user_id,
                username,
                email,
                password,
                plan
            )
            VALUES(?,?,?,?,?)
            """,
            (
                user_id,
                username,
                email,
                password,
                plan
            )
        )

    # =====================================================

    def get_user(self, username):

        return self.fetchone(
            """
            SELECT *
            FROM users
            WHERE username=?
            """,
            (username,)
        )

    # =====================================================

    def get_user_by_email(self, email):

        return self.fetchone(
            """
            SELECT *
            FROM users
            WHERE email=?
            """,
            (email,)
        )

    # =====================================================

    def get_user_by_id(self, user_id):

        return self.fetchone(
            """
            SELECT *
            FROM users
            WHERE user_id=?
            """,
            (user_id,)
        )

    # =====================================================

    def get_all_users(self):

        return self.fetchall(
            """
            SELECT *
            FROM users
            ORDER BY created_at DESC
            """
        )

    # =====================================================

    def username_exists(self, username):

        return self.get_user(username) is not None

    # =====================================================

    def email_exists(self, email):

        return self.get_user_by_email(email) is not None

    # =====================================================

    def update_password(
        self,
        user_id,
        password
    ):

        self.execute(
            """
            UPDATE users
            SET password=?
            WHERE user_id=?
            """,
            (
                password,
                user_id
            )
        )

    # =====================================================

    def update_email(
        self,
        user_id,
        email
    ):

        self.execute(
            """
            UPDATE users
            SET email=?
            WHERE user_id=?
            """,
            (
                email,
                user_id
            )
        )

    # =====================================================

    def update_avatar(
        self,
        user_id,
        avatar
    ):

        self.execute(
            """
            UPDATE users
            SET avatar=?
            WHERE user_id=?
            """,
            (
                avatar,
                user_id
            )
        )

    # =====================================================

    def update_plan(
        self,
        user_id,
        plan
    ):

        self.execute(
            """
            UPDATE users
            SET plan=?
            WHERE user_id=?
            """,
            (
                plan,
                user_id
            )
        )

    # =====================================================

    def delete_user(self, user_id):

        self.execute(
            """
            DELETE FROM users
            WHERE user_id=?
            """,
            (user_id,)
        )
            # =====================================================
    # CHAT FUNCTIONS
    # =====================================================

    def save_chat(
        self,
        user_id,
        role,
        content
    ):

        self.execute(
            """
            INSERT INTO chat_history(
                user_id,
                role,
                content
            )
            VALUES(?,?,?)
            """,
            (
                user_id,
                role,
                content
            )
        )

    # =====================================================

    def get_chat_history(self, user_id):

        return self.fetchall(
            """
            SELECT *
            FROM chat_history
            WHERE user_id=?
            ORDER BY id ASC
            """,
            (user_id,)
        )

    # =====================================================

    def clear_chat(self, user_id):

        self.execute(
            """
            DELETE FROM chat_history
            WHERE user_id=?
            """,
            (user_id,)
        )

    # =====================================================

    def delete_chat_message(self, message_id):

        self.execute(
            """
            DELETE FROM chat_history
            WHERE id=?
            """,
            (message_id,)
        )

    # =====================================================
    # MEMORY FUNCTIONS
    # =====================================================

    def save_memory(
        self,
        user_id,
        title,
        content
    ):

        self.execute(
            """
            INSERT INTO memory(
                user_id,
                title,
                content
            )
            VALUES(?,?,?)
            """,
            (
                user_id,
                title,
                content
            )
        )

    # =====================================================

    def get_memory(self, user_id):

        return self.fetchall(
            """
            SELECT *
            FROM memory
            WHERE user_id=?
            ORDER BY id DESC
            """,
            (user_id,)
        )

    # =====================================================

    def delete_memory(self, memory_id):

        self.execute(
            """
            DELETE FROM memory
            WHERE id=?
            """,
            (memory_id,)
        )

    # =====================================================
    # FAVORITES
    # =====================================================

    def add_favorite(
        self,
        user_id,
        question,
        answer
    ):

        self.execute(
            """
            INSERT INTO favorites(
                user_id,
                question,
                answer
            )
            VALUES(?,?,?)
            """,
            (
                user_id,
                question,
                answer
            )
        )

    # =====================================================

    def get_favorites(self, user_id):

        return self.fetchall(
            """
            SELECT *
            FROM favorites
            WHERE user_id=?
            ORDER BY id DESC
            """,
            (user_id,)
        )

    # =====================================================

    def remove_favorite(self, favorite_id):

        self.execute(
            """
            DELETE FROM favorites
            WHERE id=?
            """,
            (favorite_id,)
        )
            # =====================================================
    # SETTINGS
    # =====================================================

    def create_settings(self, user_id):

        if self.fetchone(
            "SELECT id FROM settings WHERE user_id=?",
            (user_id,)
        ):
            return

        self.execute(
            """
            INSERT INTO settings(
                user_id,
                theme,
                language,
                tts,
                web_search
            )
            VALUES(?,?,?,?,?)
            """,
            (
                user_id,
                "light",
                "uz",
                1,
                0
            )
        )

    # =====================================================

    def get_settings(self, user_id):

        return self.fetchone(
            """
            SELECT *
            FROM settings
            WHERE user_id=?
            """,
            (user_id,)
        )

    # =====================================================

    def update_settings(
        self,
        user_id,
        theme,
        language,
        tts,
        web_search
    ):

        self.execute(
            """
            UPDATE settings
            SET
                theme=?,
                language=?,
                tts=?,
                web_search=?
            WHERE user_id=?
            """,
            (
                theme,
                language,
                tts,
                web_search,
                user_id
            )
        )

    # =====================================================
    # STATISTICS
    # =====================================================

    def create_statistics(self, user_id):

        if self.fetchone(
            "SELECT id FROM statistics WHERE user_id=?",
            (user_id,)
        ):
            return

        self.execute(
            """
            INSERT INTO statistics(user_id)
            VALUES(?)
            """,
            (user_id,)
        )

    # =====================================================

    def increment_questions(self, user_id):

        self.execute(
            """
            UPDATE statistics
            SET questions = questions + 1
            WHERE user_id=?
            """,
            (user_id,)
        )

    # =====================================================

    def increment_images(self, user_id):

        self.execute(
            """
            UPDATE statistics
            SET images = images + 1
            WHERE user_id=?
            """,
            (user_id,)
        )

    # =====================================================

    def increment_pdfs(self, user_id):

        self.execute(
            """
            UPDATE statistics
            SET pdfs = pdfs + 1
            WHERE user_id=?
            """,
            (user_id,)
        )

    # =====================================================

    def increment_voices(self, user_id):

        self.execute(
            """
            UPDATE statistics
            SET voices = voices + 1
            WHERE user_id=?
            """,
            (user_id,)
        )

    # =====================================================

    def get_statistics(self, user_id):

        return self.fetchone(
            """
            SELECT *
            FROM statistics
            WHERE user_id=?
            """,
            (user_id,)
        )

    # =====================================================
    # DATABASE
    # =====================================================

    def close(self):
        self.conn.close()

# =====================================================
# SETTINGS
# =====================================================

    def create_settings(self, user_id):

        self.execute(
            """
            INSERT OR IGNORE INTO settings(
                user_id
            )
            VALUES(?)
            """,
            (user_id,)
        )

    # =====================================================

    def get_settings(self, user_id):

        return self.fetchone(
            """
            SELECT *
            FROM settings
            WHERE user_id=?
            """,
            (user_id,)
        )

# =====================================================
# STATISTICS
# =====================================================

    def create_statistics(self, user_id):

        self.execute(
            """
            INSERT OR IGNORE INTO statistics(
                user_id
            )
            VALUES(?)
            """,
            (user_id,)
        )

    # =====================================================

    def get_statistics(self, user_id):

        return self.fetchone(
            """
            SELECT *
            FROM statistics
            WHERE user_id=?
            """,
            (user_id,)
        )

    # =====================================================

    def increase_questions(self, user_id):

        self.execute(
            """
            UPDATE statistics
            SET questions = questions + 1
            WHERE user_id=?
            """,
            (user_id,)
        )

    # =====================================================

    def increase_pdfs(self, user_id):

        self.execute(
            """
            UPDATE statistics
            SET pdfs = pdfs + 1
            WHERE user_id=?
            """,
            (user_id,)
        )

    # =====================================================

    def increase_images(self, user_id):

        self.execute(
            """
            UPDATE statistics
            SET images = images + 1
            WHERE user_id=?
            """,
            (user_id,)
        )

    # =====================================================

    def increase_voices(self, user_id):

        self.execute(
            """
            UPDATE statistics
            SET voices = voices + 1
            WHERE user_id=?
            """,
            (user_id,)
        )
        
db = Database()

