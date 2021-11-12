from wtforms import (
    SubmitField,
    validators,
    StringField,
    SelectField,
    HiddenField,
)
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm

from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models.category import Category
from app.models.user import User

def all_categories():
    return Category.find_all_categories()

def all_users():
    return User.find_users_not_deleted_and_active()

class ComplaintForm(FlaskForm):

    "Crea el formulario para obtener datos de una denuncia"

    id = HiddenField()

    title = StringField(
        "Título (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
            validators.Regexp(
                "^[a-zA-Z ]+$",
                message="Por favor, ingrese un título válido. El título solo puede contener letras.",
            ),
        ],
        render_kw={
            "pattern": "^[a-zA-Z ]+$",
            "title": "El título solo puede contener letras",
        },
    )

    category = QuerySelectField(
        "Categoría (*)",
        query_factory=all_categories,
        get_label="name"
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

    coordinate = HiddenField()

    state = SelectField(
        "Estado",
        choices=[
            ("Sin confirmar", "Sin confirmar"),
            ("En curso", "En curso"),
            ("Resuelta", "Resuelta"),
            ("Cerrada", "Cerrada"),
        ],
        validators = [ 
            validators.DataRequired(
                message="Este campo es obligatorio"
            ), 
        ]
    )

    assigned_to = QuerySelectField(
        "Asignado a",
        query_factory=all_users,
        allow_blank=True,
        get_label="username"
    )

    creator_last_name = StringField(
        "Apellido denunciante (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
            validators.Regexp(
                "^[a-zA-Z ]+$",
                message="Por favor, ingrese un apellido válido. El apellido solo puede tener letras.",
            ),
        ],
        render_kw={
            "pattern": "^[a-zA-Z ]+$",
            "title": "El apellido solo puede tener letras",
        },
    )

    creator_first_name = StringField(
        "Nombre denunciante (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
            validators.Regexp(
                "^[a-zA-Z ]+$",
                message="Por favor, ingrese un nombre válido. El nombre solo puede tener letras.",
            ),
        ],
        render_kw={
            "pattern": "^[a-zA-Z ]+$",
            "title": "El nombre solo puede tener letras",
        },
    )

    creator_telephone = StringField(
        "Teléfono denunciante(*)",
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

    creator_email = EmailField(
        "Email denunciante(*)",
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
