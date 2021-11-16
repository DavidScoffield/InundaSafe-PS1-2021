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

    class Meta:
        locales = ['es_ES', 'es']

        def get_translations(self, form):
            return super(FlaskForm.Meta, self).get_translations(form)    

    id = HiddenField()

    name = StringField(
        "Nombre (*)",
        [
            validators.DataRequired(),
            validators.Length(max=255),
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

    description = TextAreaField("Descripción del recorrido", [ validators.Length(max=500) ])

    state = SelectField(
        "Estado",
        choices=[
            ("publicated", "Publicado"),
            ("despublicated", "Despublicado"),
        ],
        validators = [ validators.DataRequired() ]
    )

    coordinates = HiddenField()

    submit = SubmitField(
        "Guardar", render_kw={"class": "button-gradient"}
    )