from wtforms import (
    SubmitField,
    validators,
    StringField,
    PasswordField,
    RadioField,
    BooleanField,
)
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm

class EditOtherUserForm(FlaskForm):

    "Crea el formulario para editar a otro usuario"

    #id = HiddenField()

    first_name = StringField(
        "Nombre (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
            validators.Regexp(
                "^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$",
                message="Por favor, ingrese un nombre válido",
            ),
        ],
        render_kw={
            "pattern": "^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$",
            "title": "El nombre solo puede contener letras",
        },
    )

    last_name = StringField(
        "Apellido (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
            validators.Regexp(
                "^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$",
                message="Por favor, ingrese un apellido válido",
            ),
        ],
        render_kw={
            "pattern": "^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$",
            "title": "El apellido solo puede contener letras",
        },
    )

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
    )

    password = PasswordField(
        "Contraseña (*)",
        [
            validators.DataRequired(
                message="Este campo es obligatorio"
            ),
            validators.Regexp(
                "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
                message="La contraseña debe al menos 8 caracteres, una letra y un número",
            ),
        ],
        render_kw={
            "pattern": "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
            "title": "La contraseña debe al menos 8 caracteres, una letra y un número",
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
            ("bloqueado", "Bloqueado")
        ],
        default='activo'
    )

    rol_label = StringField(
        "Roles (*)",
        render_kw={
            "type":"hidden"
        },
    )

    rol_administrador = BooleanField(
        "Adminsitrador",
        render_kw={
            "value":"rol_administrador"
        },
    )

    rol_operador = BooleanField(
        "Operador",
        render_kw={
            "value":"rol_operador"
        },
    )

    submit = SubmitField(
        "Guardar", render_kw={"class": "button-gradient", "onclick":"validate_roles(event)"}
    )

    def validate_rol_label(form, field):
        if not form.data["rol_administrador"] and not form.data["rol_operador"]:
            raise validators.ValidationError("Seleccione al menos un rol")