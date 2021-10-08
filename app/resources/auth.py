
from flask import redirect, render_template, request, url_for, abort, session, flash
#from app.db import connection
from app.models.user import User


def login():
    return render_template("auth/login.html")


def authenticate():
    #conn = connection()
    params = request.form

    #user = User.find_by_email_and_pass(conn, params["email"], params["password"])
    user = User.query.filter(User.email==params["email"] and User.password==params["password"]) # first() devuelve un scalar

    print(user, flush=True)

    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_login"))

    session["user"] = params["email"]               # uso params[email] pq user es un scalar.
    flash("La sesión se inició correctamente.")
    print(session, flush=True)
    return redirect(url_for("home"))


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))
