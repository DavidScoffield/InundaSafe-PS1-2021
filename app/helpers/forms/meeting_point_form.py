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

    address = StringField("Dirección (*)", [ validators.DataRequired(), validators.Length(max=255) ])

    coordinate = HiddenField()

    telephone = StringField(
        "Teléfono",
        [
            validators.Optional(),
            validators.Length(max=50),
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
            validators.Length(max=150),
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
        validators = [ validators.DataRequired() ]
    )

    submit = SubmitField(
        "Guardar", render_kw={"class": "button-gradient"}
    )