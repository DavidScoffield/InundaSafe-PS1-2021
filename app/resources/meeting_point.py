from app.models.meeting_point import MeetingPoint
from flask import render_template, Blueprint, request, flash, redirect, url_for, session, abort
from app.db import db
from wtforms import SubmitField, validators, IntegerField, StringField, SelectField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from app.helpers.auth import authenticated
from app.helpers.check_permission import check_permission

meeting_point = Blueprint("meeting_point", __name__, url_prefix="/meeting-point")

class NewMeetingPointForm(FlaskForm):

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

    if not authenticated(session) or not check_permission("punto_encuentro_new"):
        abort(401)

    if request.method == "POST":
        form = NewMeetingPointForm(request.form)
        if not form.validate_on_submit():
            flash("Por favor, corrija los errores")
        else:
            args = form.data
            del args["submit"]
            del args["csrf_token"]
            if MeetingPoint.exists_address(args["address"]):
                flash("Ya existe un punto de encuentro con esa dirección")
            else:
                MeetingPoint.new(**args)
                flash("Punto de encuentro agregado exitosamente")
    else:
        form = NewMeetingPointForm()

    return render_template("meeting_point/new.html", form = form)

@meeting_point.route("/<int:page_number>")
def index(page_number):

    if not authenticated(session) or not check_permission("punto_encuentro_index"):
        abort(401)

    meeting_points = MeetingPoint.paginate(page_number)

    return render_template("meeting_point/index.html", meeting_points = meeting_points)

@meeting_point.route("/delete/<int:id>")
def destroy(id):

    if not authenticated(session) or not check_permission("punto_encuentro_destroy"):
        abort(401)

    MeetingPoint.delete(id)

    #flash("Punto de encuentro borrado exitosamente")

    return redirect(url_for("meeting_point.index", page_number=1))