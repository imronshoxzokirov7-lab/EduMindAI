"""
============================================================
EduMindAI Enterprise v3.0
Authentication Manager
============================================================
"""

import uuid
import bcrypt
import streamlit as st

from database import db


class AuthManager:

    def __init__(self):
        pass

    # =====================================================
    # PASSWORD
    # =====================================================

    def hash_password(self, password: str) -> str:
        hashed = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )
        return hashed.decode("utf-8")

    # =====================================================

    def verify_password(
        self,
        password: str,
        hashed: str
    ) -> bool:

        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed.encode("utf-8")
        )

    # =====================================================
    # USER REGISTER
    # =====================================================

    def register(
        self,
        username,
        email,
        password
    ):

        if db.username_exists(username):
            return False, "Bu username band."

        if db.email_exists(email):
            return False, "Bu email allaqachon mavjud."

        user_id = str(uuid.uuid4())

        password = self.hash_password(password)

        db.create_user(
            user_id=user_id,
            username=username,
            email=email,
            password=password
        )

        db.create_settings(user_id)

        db.create_statistics(user_id)

        return True, "Ro'yxatdan o'tish muvaffaqiyatli."

    # =====================================================
    # USER LOGIN
    # =====================================================

    def login(
        self,
        username,
        password
    ):

        user = db.get_user(username)

        if user is None:
            return False, "Foydalanuvchi topilmadi."

        if not self.verify_password(
            password,
            user["password"]
        ):
            return False, "Parol noto'g'ri."

        st.session_state["logged_in"] = True

        st.session_state["user_id"] = user["user_id"]

        st.session_state["username"] = user["username"]

        st.session_state["plan"] = user["plan"]

        return True, "Kirish muvaffaqiyatli."
        # =====================================================
    # LOGOUT
    # =====================================================

    def logout(self):

        keys = [
            "logged_in",
            "user_id",
            "username",
            "plan"
        ]

        for key in keys:
            if key in st.session_state:
                del st.session_state[key]

    # =====================================================
    # PROFILE
    # =====================================================

    def current_user(self):

        if "user_id" not in st.session_state:
            return None

        return db.get_user_by_id(
            st.session_state["user_id"]
        )

    # =====================================================
    # CHANGE PASSWORD
    # =====================================================

    def change_password(
        self,
        user_id,
        old_password,
        new_password
    ):

        user = db.get_user_by_id(user_id)

        if user is None:
            return False, "Foydalanuvchi topilmadi."

        if not self.verify_password(
            old_password,
            user["password"]
        ):
            return False, "Eski parol noto'g'ri."

        hashed = self.hash_password(
            new_password
        )

        db.update_password(
            user_id,
            hashed
        )

        return True, "Parol yangilandi."

    # =====================================================
    # CHANGE EMAIL
    # =====================================================

    def change_email(
        self,
        user_id,
        email
    ):

        if db.email_exists(email):
            return False, "Bu email mavjud."

        db.update_email(
            user_id,
            email
        )

        return True, "Email yangilandi."

    # =====================================================
    # CHANGE AVATAR
    # =====================================================

    def change_avatar(
        self,
        user_id,
        avatar
    ):

        db.update_avatar(
            user_id,
            avatar
        )

        return True

    # =====================================================
    # CHANGE PLAN
    # =====================================================

    def change_plan(
        self,
        user_id,
        plan
    ):

        db.update_plan(
            user_id,
            plan
        )

        st.session_state["plan"] = plan

        return True
        # =====================================================
    # DELETE ACCOUNT
    # =====================================================

    def delete_account(
        self,
        user_id
    ):

        user = db.get_user_by_id(user_id)

        if user is None:
            return False, "Foydalanuvchi topilmadi."

        db.delete_user(user_id)

        self.logout()

        return True, "Account o'chirildi."

    # =====================================================
    # ADMIN
    # =====================================================

    def is_admin(self):

        if "username" not in st.session_state:
            return False

        admin_users = [
            "admin",
            "Imronbek",
            "imronbek"
        ]

        return (
            st.session_state["username"]
            in admin_users
        )

    # =====================================================
    # LOGIN CHECK
    # =====================================================

    def is_logged_in(self):

        return st.session_state.get(
            "logged_in",
            False
        )

    # =====================================================
    # REQUIRE LOGIN
    # =====================================================

    def require_login(self):

        if not self.is_logged_in():

            st.warning(
                "Avval tizimga kiring."
            )

            st.stop()

    # =====================================================
    # USER PLAN
    # =====================================================

    def current_plan(self):

        return st.session_state.get(
            "plan",
            "Free"
        )

    # =====================================================
    # PREMIUM CHECK
    # =====================================================

    def is_premium(self):

        return self.current_plan() in [

            "Pro",

            "Enterprise"

        ]

    # =====================================================
    # ENTERPRISE CHECK
    # =====================================================

    def is_enterprise(self):

        return self.current_plan() == "Enterprise"

    # =====================================================
    # USER STATISTICS
    # =====================================================

    def statistics(self):

        if "user_id" not in st.session_state:
            return None

        return db.get_statistics(
            st.session_state["user_id"]
        )


# =====================================================
# AUTH OBJECT
# =====================================================

auth = AuthManager()

