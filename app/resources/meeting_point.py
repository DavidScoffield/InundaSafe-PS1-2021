from app.models.meeting_point import MeetingPoint
from flask import (
    render_template,
    Blueprint,
    request,
    flash,
    redirect,
    url_for,
    session,
    abort,
)
from app.db import db
from wtforms import (
    SubmitField,
    validators,
    IntegerField,
    StringField,
    SelectField,
)
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from app.helpers.auth import authenticated
from app.helpers.check_permission import check_permission
from app.helpers.check_param_search_meeting_point import (
    check_param,
)

meeting_point = Blueprint(
    "meeting_point", __name__, url_prefix="/meeting-point"
)


class NewMeetingPointForm(FlaskForm):

    "Crea el formulario para dar de alta a un meeting point"

    name = StringField(
        "Nombre (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
            validators.Regexp(
                "^[a-z A-Z]+$",
                message="Por favor, ingrese un nombre válido",
            ),
        ],
        render_kw={
            "pattern": "[a-z A-Z]+$",
            "title": "El nombre no puede contener números",
        },
    )

    address = StringField(
        "Dirección (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            )
        ],
    )

    coor_X = StringField(
        "Coordenada X",
        [
            validators.Optional(),
            validators.Regexp(
                "^[\d]+$",
                message="Por favor, ingrese una coordenada X válida",
            ),
        ],
        render_kw={
            "pattern": "^[\d]+$",
            "title": "La coordenada no puede contener letras",
        },
    )

    coor_Y = StringField(
        "Coordenada Y",
        [
            validators.Optional(),
            validators.Regexp(
                "^[\d]+$",
                message="Por favor, ingrese una coordenada Y válida",
            ),
        ],
        render_kw={
            "pattern": "^[\d]+$",
            "title": "La coordenada no puede contener letras",
        },
    )

    telephone = StringField(
        "Teléfono",
        [
            validators.Optional(),
            validators.Regexp(
                "^[\d]+$",
                message="Por favor, ingrese un número de teléfono válido",
            ),
        ],
        render_kw={
            "pattern": "^[\d]+$",
            "title": "El teléfono no puede contener letras",
        },
    )

    email = EmailField(
        "Email",
        [
            validators.Email(
                message="Por favor, ingrese un email válido"
            ),
            validators.Optional(),
        ],
    )

    state = SelectField(
        "Estado",
        choices=[
            ("publicated", "Publicado"),
            ("despublicated", "Despublicado"),
        ],
    )

    submit = SubmitField(
        "Guardar", render_kw={"class": "button-gradient"}
    )


@meeting_point.get("/new")
def new():
    "Controller para mostrar el formulario para el alta de un punto de encuentro"

    if not authenticated(session) or not check_permission(
        "punto_encuentro_new"
    ):
        abort(401)

    form = NewMeetingPointForm()

    return render_template(
        "meeting_point/new.html", form=form
    )


@meeting_point.post("/new")
def create():
    "Controller para crear el punto de encuentro a partir de los datos del formulario"

    if not authenticated(session) or not check_permission(
        "punto_encuentro_create"
    ):
        abort(401)

    form = NewMeetingPointForm(request.form)
    if not form.validate_on_submit():
        flash("Por favor, corrija los errores")
    else:
        args = form.data
        del args["submit"]
        del args["csrf_token"]
        if MeetingPoint.exists_address(args["address"]):
            flash(
                "Ya existe un punto de encuentro con esa dirección"
            )
        else:
            MeetingPoint.new(**args)
            flash(
                "Punto de encuentro agregado exitosamente"
            )

    return redirect(url_for("meeting_point.new"))


@meeting_point.get("/<int:page_number>")
def index(page_number):
    """
    Controller para mostrar el listado de puntos de encuentro
    Recibe como parametro el numero de la pagina a mostrar
    Puede recibir como argumentos:
    - name : string -> campo de filtro para los nombres de puntos de encuentro
    - state : string -> campo de filtro para los estados(publicado, despublicado) de puntos de encuentro
    """

    if not authenticated(session) or not check_permission(
        "punto_encuentro_index"
    ):
        abort(401)

    args = request.args
    name = args.get("name")
    state = args.get("state")

    name = check_param("name", name)
    state = check_param("state", state)

    meeting_points = MeetingPoint.search(
        page_number=page_number,
        state=state,
        name=name,
    )

    # En caso que no encuentre ningun resultado resultado se redirige a la pagina 1 con los argumentos de busqueda
    if (
        meeting_points.page != 1
        and meeting_points.page > meeting_points.pages
    ):
        # Si la cantidad de paginas es 0, se redirigira a la pagina 1
        if meeting_points.pages > 0:
            page = meeting_points.pages
        else:
            page = 1

        return redirect(
            url_for(
                "meeting_point.index",
                page_number=page,
                **request.args
            )
        )

    return render_template(
        "meeting_point/index.html",
        meeting_points=meeting_points,
    )


@meeting_point.post("/delete")
def destroy():

    if not authenticated(session) or not check_permission(
        "punto_encuentro_destroy"
    ):
        abort(401)

    MeetingPoint.delete(request.form["id_meeting_point"])

    flash("Punto de encuentro borrado exitosamente")

    return redirect(
        url_for("meeting_point.index", page_number=1)
    )
