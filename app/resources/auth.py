from flask import redirect, render_template, request, url_for, abort, session, flash
#from app.db import connection
from app.models.user import User


def login():
    return render_template("auth/login.html")


def authenticate():
    #conn = connection()
    params = request.form

    #user = User.find_by_email_and_pass(conn, params["email"], params["password"])
    #user = User.query.filter(User.email==params["email"] and User.password==params["password"]).first()
    user = User.find_by_email_and_pass(params["email"], params["password"])
    
    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_login"))
    
    if user.active == 0:
        flash("El usuario esta bloqueado")
        return redirect(url_for("auth_login"))

    permisos = []
    for rol in user.roles:
        for permiso in rol.permissions:
            permisos.append(permiso.name)

    session["user"] = user.id
    session["permissions"] = permisos
    flash("La sesión se inició correctamente.")

    return redirect(url_for("home"))


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))
