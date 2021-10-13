from app.models.meeting_point import MeetingPoint
from flask import render_template, Blueprint, request, flash, redirect, url_for, session, abort
from app.db import db
from wtforms import SubmitField, validators, IntegerField, StringField, SelectField
from wtforms.fields.html5 import EmailField
from flask_wtf import Form
from app.helpers.auth import authenticated
from app.helpers.check_permission import check_permission

meeting_point = Blueprint("meeting_point", __name__, url_prefix="/meeting-point")

class NewMeetingPointForm(Form):

    "Crea el formulario para dar de alta a un meeting point"

    name = StringField('Nombre (*)', [validators.DataRequired(message = "Este campo es obligatorio"), 
                                      validators.Regexp('^[a-z A-Z]+$', message = "Por favor, ingrese un nombre válido")],
                        render_kw={"pattern" : "[a-z A-Z]+$", "title" : "El nombre no puede contener números"})
    
    address = StringField('Dirección (*)', [validators.DataRequired(message = "Este campo es obligatorio")])

    coor_X = StringField('Coordenada X', [validators.Optional(), validators.Regexp('^[\d]+$', message = "Por favor, ingrese una coordenada X válida")],
                          render_kw={"pattern" : "^[\d]+$", "title" : "La coordenada no puede contener letras"})

    coor_Y = StringField('Coordenada Y', [validators.Optional(), validators.Regexp('^[\d]+$', message = "Por favor, ingrese una coordenada Y válida")],
                          render_kw={"pattern" : "^[\d]+$", "title" : "La coordenada no puede contener letras"})

    telephone = StringField('Teléfono', [validators.Optional(), validators.Regexp('^[\d]+$', message = "Por favor, ingrese un número de teléfono válido")],
                            render_kw={"pattern" : "^[\d]+$", "title" : "El teléfono no puede contener letras"})

    email = EmailField('Email', [validators.Email(message = "Por favor, ingrese un email válido"), validators.Optional()])

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




