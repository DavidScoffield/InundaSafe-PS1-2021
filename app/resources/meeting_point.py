from app.models.meeting_point import MeetingPoint
from flask import render_template, Blueprint, request
from app.db import db

meeting_point = Blueprint("meeting_point", __name__, url_prefix="/meeting-point")

