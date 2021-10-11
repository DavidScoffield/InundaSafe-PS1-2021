from app.models.meeting_point import MeetingPoint
from flask import render_template, Blueprint, request, flash, redirect, url_for
from app.db import db
from wtforms import SubmitField, validators, IntegerField, StringField, SelectField
from flask_wtf import Form

meeting_point = Blueprint("meeting_point", __name__, url_prefix="/meeting-point")

class NewMeetingPointForm(Form):
    name = StringField('Nombre', [validators.DataRequired(message = "Este campo es obligatorio"), validators.Regexp('^[a-z A-Z]+$', message = "Por favor, ingrese un nombre válido")])
    address = StringField('Dirección', [validators.DataRequired(message = "Este campo es obligatorio")])
    coor_X = StringField('Coordenada X', [validators.Optional(), validators.Regexp('^[\d]+$', message = "Por favor, ingrese una coordenada X válida")])
    coor_Y = StringField('Coordenada Y', [validators.Optional(), validators.Regexp('^[\d]+$', message = "Por favor, ingrese una coordenada Y válida")])
    telephone = StringField('Teléfono', [validators.Optional(), validators.Regexp('^[\d]+$', message = "Por favor, ingrese un número de teléfono válido")])
    email = StringField('Email', [validators.Email(message = "Por favor, ingrese un email válido"), validators.Optional()])
    state = SelectField('Estado', choices = [("publicated", "Publicado"), ("despublicated", "Despublicado")])
    submit = SubmitField('Guardar', render_kw={'class':'button-gradient'})

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
