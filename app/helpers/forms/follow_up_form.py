from wtforms import (
    SubmitField,
    validators,
    StringField,
    HiddenField,
)
from flask_wtf import FlaskForm


class FollowUpForm(FlaskForm):

    "Crea el formulario para obtener datos de un seguimiento"

    id = HiddenField()

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
            validators.Length(
                max=400, 
                message="La descripción no puede ser tan larga",
            ),
        ],
        render_kw={
            "pattern": "^[a-zA-Z0-9 ]+$",
            "title": "La descripción no puede tener caracteres especiales",
            "maxlength": "400",
        },
    )

    id_complaint = HiddenField()

    submit = SubmitField(
        "Guardar", render_kw={"class": "button-gradient"}
    )
