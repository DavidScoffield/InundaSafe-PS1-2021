from app.models.meeting_point import MeetingPoint
from flask import render_template, Blueprint, request, flash, redirect, url_for, session, abort
from app.db import db
from wtforms import SubmitField, validators, IntegerField, StringField, SelectField
from flask_wtf import Form
from app.helpers.auth import authenticated
from app.helpers.check_permission import check_permission

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

    #if not authenticated(session):
        #abort(401)

    #if (not check_permission("usuario_index")):
        #abort(401)

    if request.method == "POST":
        form = NewMeetingPointForm(request.form)
        if not form.validate_on_submit():
            flash("Por favor, corrija los errores")
        else:
            args = form.data
            del args["submit"]
            del args["csrf_token"]
            MeetingPoint.new(**args)
            flash("Punto de encuentro agregado exitosamente")
    else:
        form = NewMeetingPointForm()

    return render_template("meeting_point/new.html", form = form)




