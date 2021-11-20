from wtforms import (
    SubmitField,
    validators,
    StringField,
    SelectField,
    HiddenField,
)
from flask_wtf import FlaskForm
from wtforms.widgets.html5 import ColorInput


class FloodZoneForm(FlaskForm):

    "Crea el formulario para zonas inundables"

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

    cipher = StringField(
        "Código",
        render_kw={"readonly": True},
    )

    state = SelectField(
        "Estado",
        choices=[
            ("publicated", "Publicado"),
            ("despublicated", "Despublicado"),
        ],
        validators=[
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
        ],
    )

    color = StringField(
        "Color",
        [
            validators.Optional(),
            validators.Regexp(
                "^#(([\da-fA-F]{3}){1,2}|([\da-fA-F]{4}){1,2})$",
                message="Por favor, ingrese un dato válido. Debe ingresarse un valor hexadecimal.",
            ),
        ],
        render_kw={
            "pattern": "^#(([\da-fA-F]{3}){1,2}|([\da-fA-F]{4}){1,2})$",
            "title": "El color debe ser un valor hexadecimal",
            "placeholder": "#F5FF70",
        },
        widget=ColorInput(),
    )

    coordinates = HiddenField()

    submit = SubmitField(
        "Guardar",
        render_kw={"class": "btn button-gradient"},
    )
