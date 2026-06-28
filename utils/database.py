"""
Oddiy JSON-based ma'lumotlar bazasi
Railway'da SQLite o'rniga PostgreSQL ishlatish tavsiya etiladi
"""
import json
import os
from datetime import datetime

DB_FILE = "data/users.json"


def init_db():
    """Ma'lumotlar bazasini ishga tushirish"""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)


def get_user(user_id):
    """Foydalanuvchi ma'lumotlarini olish"""
    init_db()
    with open(DB_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
    return users.get(str(user_id), {})


def save_user(user_id, data):
    """Foydalanuvchi ma'lumotlarini saqlash"""
    init_db()
    with open(DB_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)

    users[str(user_id)] = data

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def create_user(user_id, username=None, first_name=None):
    """Yangi foydalanuvchi yaratish"""
    user_data = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "level": "beginner",
        "points": 0,
        "lessons_completed": 0,
        "exercises_completed": 0,
        "joined_date": datetime.now().isoformat(),
        "last_active": datetime.now().isoformat(),
        "settings": {
            "notifications": True,
            "language": "uz"
        }
    }
    save_user(user_id, user_data)
    return user_data


def update_user(user_id, **kwargs):
    """Foydalanuvchi ma'lumotlarini yangilash"""
    user = get_user(user_id)
    if not user:
        return None

    for key, value in kwargs.items():
        if key in user:
            user[key] = value
        elif key in user.get("settings", {}):
            user["settings"][key] = value

    user["last_active"] = datetime.now().isoformat()
    save_user(user_id, user)
    return user


def add_points(user_id, points):
    """Foydalanuvchiga ball qo'shish"""
    user = get_user(user_id)
    if user:
        user["points"] = user.get("points", 0) + points
        save_user(user_id, user)
    return user


def get_all_users():
    """Barcha foydalanuvchilarni olish (admin uchun)"""
    init_db()
    with open(DB_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
    return users


def get_stats():
    """Umumiy statistika"""
    users = get_all_users()
    total = len(users)
    active_today = 0
    today = datetime.now().date()

    for user in users.values():
        last_active = datetime.fromisoformat(user.get("last_active", "2000-01-01"))
        if last_active.date() == today:
            active_today += 1

    return {
        "total_users": total,
        "active_today": active_today,
        "total_points": sum(u.get("points", 0) for u in users.values())
    }
