from wtforms import (
    SubmitField,
    validators,
    StringField,
    RadioField,
    BooleanField,
)
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from wtforms.fields.simple import HiddenField


class ApproveUserForm(FlaskForm):

    "Crea el formulario para aprobar a un usuario"

    # id = HiddenField()

    email = EmailField(
        "Email (*)",
        [
            validators.Email(
                message="Por favor, ingrese un email válido"
            ),
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
        ],
        render_kw={"readonly": True},
    )

    first_name = StringField(
        "Nombre (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
            validators.Regexp(
                "^[a-zA-ZÀ-ÿ\u00f1\u00d1]+([a-zA-ZÀ-ÿ\u00f1\u00d1 ])*$",
                message="Por favor, ingrese un nombre válido",
            ),
        ],
        render_kw={
            "pattern": "^[a-zA-ZÀ-ÿ\u00f1\u00d1]+([a-zA-ZÀ-ÿ\u00f1\u00d1 ])*$",
            "title": "El nombre solo puede contener letras",
            "readonly": True,
        },
    )

    last_name = StringField(
        "Apellido (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
            validators.Regexp(
                "^[a-zA-ZÀ-ÿ\u00f1\u00d1]+([a-zA-ZÀ-ÿ\u00f1\u00d1 ])*$",
                message="Por favor, ingrese un apellido válido",
            ),
        ],
        render_kw={
            "pattern": "^[a-zA-ZÀ-ÿ\u00f1\u00d1]+([a-zA-ZÀ-ÿ\u00f1\u00d1 ])*$",
            "title": "El apellido solo puede contener letras",
            "readonly": True,
        },
    )

    suggested_username = StringField(
        "Nombre de usuario (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
            validators.Regexp(
                "^[a-z A-Z 0-9]+$",
                message="Por favor, ingrese un nombre de usuario válido",
            ),
        ],
        render_kw={
            "pattern": "[a-z A-Z 0-9]+$",
            "title": "El nombre de usuario solo puede contener letras y números",
        },
    )

    active = RadioField(
        "Estado (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            )
        ],
        choices=[
            ("activo", "Activo"),
            ("bloqueado", "Bloqueado"),
        ],
        default="activo",
    )

    rol_label = StringField(
        "Roles (*)",
        render_kw={"type": "hidden"},
    )

    rol_administrador = BooleanField(
        "Adminsitrador",
        render_kw={"value": "rol_administrador"},
    )

    rol_operador = BooleanField(
        "Operador",
        render_kw={"value": "rol_operador"},
    )

    submit = SubmitField(
        "Aprobar Usuario",
        render_kw={
            "class": "button-gradient",
        },
    )

    def validate_rol_label(form, field):
        if (
            not form.data["rol_administrador"]
            and not form.data["rol_operador"]
        ):
            raise validators.ValidationError(
                "Seleccione al menos un rol"
            )
