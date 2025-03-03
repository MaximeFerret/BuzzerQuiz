from datetime import datetime, timedelta, timezone

from backend.dao.auth_dao import UserDAO
from backend.models.db import db
from flask_login import login_user
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class AuthService:
    @staticmethod
    def create_user(username, email, password):
        """创建用户并保存"""
        password_hash = bcrypt.generate_password_hash(password)
        new_user = UserDAO.create_user(username, email, password_hash)
        return new_user

    @staticmethod
    def authenticate_user(email, password):
        """认证用户"""
        user = UserDAO.get_user_by_email(email)

        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return None

        return user
    
    @staticmethod
    def get_user_by_email(email):
        """根据邮箱查找用户"""
        return UserDAO.get_user_by_email(email)

    @staticmethod
    def set_user_session(user_id):
        """设置用户会话"""
        return {
            "is_user": True,
            "user_last_active": datetime.now(timezone.utc),
            "user_id": user_id,
        }

    @staticmethod
    def set_admin_session():
        """设置管理员会话"""
        return {"is_admin": True, "admin_last_active": datetime.now(timezone.utc)}

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
        if not last_active:
            return True
        return datetime.now(timezone.utc) - last_active > timedelta(minutes=timeout)
