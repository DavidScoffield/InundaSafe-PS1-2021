from wtforms import (
    SubmitField,
    validators,
    StringField,
    PasswordField,
    BooleanField,
)
from wtforms.fields.core import SelectField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm

class EditMyProfileForm(FlaskForm):

    "Crea el formulario para editar mi perfil"

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
        "Contraseña",
        [
            validators.Optional(),
            validators.Regexp(
                "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
                message="La contraseña debe tener al menos 8 caracteres, una letra y un número",
            ),
        ],
        render_kw={
            "pattern": "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
            "title": "La contraseña debe tener al menos 8 caracteres, una letra y un número",
        },
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
            "value":"rol_administrador", "onclick":"confirm_uncheck_admin(event)"
        },
    )

    rol_operador = BooleanField(
        "Operador",
        render_kw={
            "value":"rol_operador"
        },
    )

    submit = SubmitField(
        "Guardar", render_kw={"class": "btn button-gradient", "onclick":"validate_roles(event)"}
    )

    def validate_rol_label(form, field):
        if not form.data["rol_administrador"] and not form.data["rol_operador"]:
            raise validators.ValidationError("Seleccione al menos un rol")