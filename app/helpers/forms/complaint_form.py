from wtforms import (
    SubmitField,
    validators,
    StringField,
    SelectField,
    HiddenField,
)
from wtforms.fields.html5 import EmailField
from wtforms.widgets import HiddenInput
from flask_wtf import FlaskForm


class ComplaintForm(FlaskForm):

    "Crea el formulario para obtener datos de un meeting point"

    #id = HiddenField()

    title = StringField(
        "Título (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
            validators.Regexp(
                "^[a-zA-Z0-9 ]+$",
                message="Por favor, ingrese un título válido. El título no puede tener caracteres especiales.",
            ),
        ],
        render_kw={
            "pattern": "^[a-zA-Z0-9 ]+$",
            "title": "El título no puede tener caracteres especiales",
        },
    )

    category = SelectField(
        "Categoría (*)",
        choices=[
            ("sewer", "Alcantarilla tapada"),
            ("garbage_dump", "Basural"),
            #agregar más categorías
        ],
        validators = [ validators.DataRequired(
                        message="Este campo es obligatorio"
                      ), ]
    )

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

    coordinates = HiddenField()

    state = SelectField(
        "Estado",
        choices=[
            ("not_confirm", "Sin confirmar"),
            ("in_course", "En curso"),
            ("resolved", "Resuelta"),
            ("closed", "Cerrada"),
        ],
        validators = [ validators.DataRequired(
                        message="Este campo es obligatorio"
                      ), ]
    )

    state = SelectField(
        "Asignado a",
        choices=[
            ("not_confirm", "NO SE QUE OPCIONES"),
            ("in_course", "PONER"),
            #no se que opciones tendrian que ir
        ],
        validators = [ validators.DataRequired(
                        message="Este campo es obligatorio"
                      ), ]
    )

    last_name = StringField(
        "Apellido denunciante (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
            validators.Regexp(
                "^[a-zA-Z0-9 ]+$",
                message="Por favor, ingrese un apellido válido. El apellido no puede tener caracteres especiales.",
            ),
        ],
        render_kw={
            "pattern": "^[a-zA-Z0-9 ]+$",
            "title": "El apellido no puede tener caracteres especiales",
        },
    )

    first_name = StringField(
        "Nombre denunciante (*)",
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

    telephone = StringField(
        "Teléfono (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
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
        "Email (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
            validators.Email(
                message="Por favor, ingrese un email válido"
            ),
        ],
    )

    submit = SubmitField(
        "Guardar", render_kw={"class": "button-gradient"}
    )
