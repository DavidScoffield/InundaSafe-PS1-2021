from app.models.meeting_point import MeetingPoint
from flask import render_template, Blueprint, request, flash
from app.db import db

meeting_point = Blueprint("meeting_point", __name__, url_prefix="/meeting-point")

@meeting_point.route("/new", methods = ['GET','POST'])
def new():

    if request.method == "POST":

        try:
            MeetingPoint.meeting_point_new(**request.form)
        except:
            flash("El nombre y la dirección del punto de encuentro son campos obligatorios")
        else:
            flash("Punto de encuentro agregado exitosamente")

    return render_template("meeting_point/new.html")