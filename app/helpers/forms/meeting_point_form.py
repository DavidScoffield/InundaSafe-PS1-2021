from wtforms import SubmitField, validators, IntegerField, StringField, SelectField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm

class MeetingPointForm(FlaskForm):

    "Crea el formulario para obtener datos de un meeting point"

    name = StringField(
        "Nombre (*)",
        [
            validators.DataRequired(message="Este campo es obligatorio"),
            validators.Regexp(
                "^[a-z A-Z]+$", message="Por favor, ingrese un nombre válido"
            ),
        ],
        render_kw={
            "pattern": "[a-z A-Z]+$",
            "title": "El nombre no puede contener números",
        },
    )

    address = StringField(
        "Dirección (*)", [validators.DataRequired(message="Este campo es obligatorio")]
    )

    coor_X = StringField(
        "Coordenada X",
        [
            validators.Optional(),
            validators.Regexp(
                "^[\d]+$", message="Por favor, ingrese una coordenada X válida"
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
                "^[\d]+$", message="Por favor, ingrese una coordenada Y válida"
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
                "^[\d]+$", message="Por favor, ingrese un número de teléfono válido"
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
            validators.Email(message="Por favor, ingrese un email válido"),
            validators.Optional(),
        ],
    )

    state = SelectField(
        "Estado",
        choices=[("publicated", "Publicado"), ("despublicated", "Despublicado")],
    )

    submit = SubmitField("Guardar", render_kw={"class": "button-gradient"})