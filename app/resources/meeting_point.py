from app.models.meeting_point import MeetingPoint
from flask import render_template, Blueprint, request
from app.db import db

meeting_point = Blueprint("meeting_point", __name__, url_prefix="/meeting-point")

@meeting_point.route("/new", methods = ['GET','POST'])
def new():

    if request.method == "POST":

        MeetingPoint.meeting_point_new(**request.form)

    return render_template("meeting_point/new.html")