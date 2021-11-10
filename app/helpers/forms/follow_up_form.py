from wtforms import (
    SubmitField,
    validators,
    StringField,
    HiddenField,
)
from flask_wtf import FlaskForm


class FollowUpForm(FlaskForm):

    "Crea el formulario para obtener datos de un seguimiento"

    description = StringField(
        "Descripción (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
            validators.Regexp(
                "^[a-zA-Z0-9 ]+$",
                message="Por favor, ingrese una descripción válida. La descripción no puede tener caracteres especiales.",
            ),
        ],
        render_kw={
            "pattern": "^[a-zA-Z0-9 ]+$",
            "title": "La descripción no puede tener caracteres especiales",
        },
    )

    id_complaint = HiddenField()

    submit = SubmitField(
        "Guardar", render_kw={"class": "button-gradient"}
    )
