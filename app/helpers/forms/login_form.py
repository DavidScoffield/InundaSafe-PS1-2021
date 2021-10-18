from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    validators,
    PasswordField,
)
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):

    "Crea el formulario para iniciar sesion"

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

    submit = SubmitField(
        "Iniciar Sesión",
        render_kw={"class": "button-gradient"},
    )
