from datetime import datetime, timedelta
from config.settings import ADMIN_IDS, MAX_FREE_USERS

# Simulated database
user_db = {}

class UserManager:
    """Handles user authentication and authorization"""
    
    @staticmethod
    def is_admin(user_id: int) -> bool:
        return user_id in ADMIN_IDS

    @staticmethod
    def is_subscribed(user_id: int) -> bool:
        user = user_db.get(user_id, {})
        if user.get("is_admin", False):
            return True
        expiry = user.get("subscription_expiry")
        return expiry and expiry > datetime.now()

    @staticmethod
    def add_free_user(user_id: int) -> bool:
        free_users = sum(1 for u in user_db.values() if not u.get("is_subscribed", True))
        if free_users >= MAX_FREE_USERS:
            return False

        user_db[user_id] = {"is_subscribed": False, "subscription_expiry": None}
        return True

    @staticmethod
    def add_subscribed_user(user_id: int, duration_days: int = 30):
        current_expiry = user_db.get(user_id, {}).get("subscription_expiry", datetime.now())
        user_db[user_id] = {
            "is_subscribed": True,
            "subscription_expiry": current_expiry + timedelta(days=duration_days),
        }

    @staticmethod
    def get_user_stats() -> dict:
        total = len(user_db)
        subscribed = sum(1 for u in user_db.values() if u.get("is_subscribed"))
        return {
            "total_users": total,
            "subscribed_users": subscribed,
            "free_users": total - subscribed
        }