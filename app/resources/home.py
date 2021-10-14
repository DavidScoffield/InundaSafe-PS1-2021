from flask import Blueprint, redirect, url_for, render_template, session
from app.helpers.auth import authenticated

home = Blueprint("home", __name__, url_prefix="/")


@home.get("/")
def index():

    if not authenticated(session):
        return redirect(url_for("auth_routes.auth_login"))

    return render_template("home.html")
