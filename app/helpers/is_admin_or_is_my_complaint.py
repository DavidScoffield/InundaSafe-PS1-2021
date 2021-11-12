from flask import session
from app.models.user import User
from app.helpers.has_role import has_role

def is_admin_or_is_my_complaint(complaint):
    """Devuelve True si este usuario es Admin o si es el asignado a la denuncia pasada por parametro"""

    this_user = User.find_user_by_id(session["user"])

    is_admin = has_role(this_user.roles, "rol_administrador")
    is_my_complaint = complaint.assigned_to == session["user"]

    return is_admin or is_my_complaint