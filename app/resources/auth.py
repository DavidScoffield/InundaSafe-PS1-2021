from flask import redirect, render_template, request, url_for, abort, session, flash
from app.models.user import User


def login():
    return render_template("auth/login.html")


def authenticate():
    params = request.form
    email = params["email"]
    password = params["password"]

    user = User.find_by_email_and_pass(email, password)

    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_login"))

    if not email or not password:
        flash("Se deben completar todos los campos")
        return redirect(url_for("auth_login"))

    if user.active == 0:
        flash("El usuario esta bloqueado")
        return redirect(url_for("auth_login"))

    permisos = []
    for rol in user.roles:
        for permiso in rol.permissions:
            permisos.append(permiso.name)
    permisos = set(permisos)

    session["user"] = user.id
    session["permissions"] = permisos
    flash("La sesión se inició correctamente.")

    return redirect(url_for("home_private"))


def login_private():
    return render_template("home_private.html")


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))
