from wtforms import (
    SubmitField,
    validators,
    IntegerField,
    StringField,
    SelectField,
    HiddenField,
)
from wtforms.fields.html5 import EmailField
from wtforms.widgets import HiddenInput
from flask_wtf import FlaskForm


class MeetingPointForm(FlaskForm):

    "Crea el formulario para obtener datos de un meeting point"

    id = HiddenField()

    name = StringField(
        "Nombre (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
            validators.Regexp(
                "^[a-zA-Z0-9 ]+$",
                message="Por favor, ingrese un nombre válido. El nombre no puede tener caracteres especiales.",
            ),
        ],
        render_kw={
            "pattern": "^[a-zA-Z0-9 ]+$",
            "title": "El nombre no puede tener caracteres especiales",
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
                "^-?[0-9]{1,10}(?:\.[0-9]+)?$",
                message="Por favor, ingrese una coordenada X válida",
            ),
        ],
        render_kw={
            "pattern": "^-?[0-9]{1,10}(?:\.[0-9]+)?$",
            "title": "Por favor, ingrese una coordenada X válida",
        },
    )

    coor_Y = StringField(
        "Coordenada Y",
        [
            validators.Optional(),
            validators.Regexp(
                "^-?[0-9]{1,10}(?:\.[0-9]+)?$",
                message="Por favor, ingrese una coordenada Y válida",
            ),
        ],
        render_kw={
            "pattern": "^-?[0-9]{1,10}(?:\.[0-9]+)?$",
            "title": "Por favor, ingrese una coordenada Y válida",
        },
    )

    telephone = StringField(
        "Teléfono",
        [
            validators.Optional(),
            validators.Regexp(
                "^[\d]+$",
                message="Por favor, ingrese un número de teléfono válido. El teléfono solo puede contener números.",
            ),
        ],
        render_kw={
            "pattern": "^[\d]+$",
            "title": "El teléfono solo puede contener números",
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
        validators = [ validators.DataRequired(
                        message="Este campo es obligatorio"
                      ), ]
    )

    submit = SubmitField(
        "Guardar", render_kw={"class": "button-gradient"}
    )
