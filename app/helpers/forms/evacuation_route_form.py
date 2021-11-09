from wtforms import (
    SubmitField,
    validators,
    StringField,
    SelectField,
    HiddenField,
    TextAreaField
)
from flask_wtf import FlaskForm


class EvacuationRouteForm(FlaskForm):

    "Crea el formulario para obtener datos de un recorrido de evacuación"

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

    description = TextAreaField("Descripción del recorrido")

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

    coordinates = HiddenField()

    submit = SubmitField(
        "Guardar", render_kw={"class": "button-gradient"}
    )