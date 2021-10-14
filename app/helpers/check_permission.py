from flask import session

def check_permission(permission):
    return permission in session["permissions"]