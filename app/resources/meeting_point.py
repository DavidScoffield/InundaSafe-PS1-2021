from app.models.meeting_point import MeetingPoint
from flask import render_template, Blueprint, request, flash, redirect, url_for
from app.db import db
from app.helpers.validators import is_empty

meeting_point = Blueprint("meeting_point", __name__, url_prefix="/meeting-point")

@meeting_point.route("/new", methods = ['GET','POST'])
def new():

    if request.method == "POST":
        args = request.form
        if is_empty(args["name"]) or is_empty(args["address"]):
            flash("El nombre y la dirección del punto de encuentro son campos obligatorios")
        else:
            MeetingPoint.new(**args)
            flash("Punto de encuentro agregado exitosamente")

    return render_template("meeting_point/new.html")