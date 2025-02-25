from app.backend.dao.auth_dao import UserDAO
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from app.backend.models import db
from datetime import datetime, timedelta

class AuthService:
    @staticmethod
    def create_user(username, email, password):
        """创建用户并保存"""
        password_hash = generate_password_hash(password)
        new_user = UserDAO.create_user(username, email, password_hash)
        return new_user

    @staticmethod
    def authenticate_user(email, password):
        """认证用户"""
        user = UserDAO.get_user_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None
    
    @staticmethod
    def set_user_session(user_id):
        """设置用户会话"""
        return {
            "is_user": True,
            "user_last_active": datetime.now(timezone.utc),
            "user_id": user_id
        }

    @staticmethod
    def set_admin_session():
        """设置管理员会话"""
        return {
            "is_admin": True,
            "admin_last_active": datetime.now(timezone.utc)
        }

    @staticmethod
    def reset_user_session():
        """重置用户会话"""
        return {"is_user": None, "user_last_active": None}

    @staticmethod
    def reset_admin_session():
        """重置管理员会话"""
        return {"is_admin": None, "admin_last_active": None}

    @staticmethod
    def check_session_expiry(last_active, timeout=10):
        """检查会话是否过期"""
        return datetime.now(timezone.utc) - last_active > timedelta(minutes=timeout)