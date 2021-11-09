from flask import session
from app.helpers.auth import authenticated
from app.models.user import User


def logged_user_info():
    user_id = authenticated(session)
    user = User.find_user_by_id(user_id)
    
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "username": user.username,
    }
