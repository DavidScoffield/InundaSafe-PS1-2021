from wtforms import (
    SubmitField,
    validators,
    IntegerField,
    StringField,
    SelectField,
    HiddenField,
    ValidationError,
)
from wtforms.fields.html5 import EmailField
from wtforms.widgets import HiddenInput
from flask_wtf import FlaskForm
from app.models.meeting_point import MeetingPoint
from app.helpers.validate_coordinates import (
    validate_json_coordinate_list,
)


class MeetingPointForm(FlaskForm):
    "Crea el formulario para obtener datos de un meeting point"

    class Meta:
        locales = ["es_ES", "es"]

        def get_translations(self, form):
            return super(
                FlaskForm.Meta, self
            ).get_translations(form)

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

    address = StringField(
        "Dirección (*)",
        [
            validators.DataRequired(),
            validators.Length(max=255),
        ],
    )

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
        validators=[validators.DataRequired()],
        # render_kw={"size": 2, "class": "no-scroll"},
        # default="publicated",
    )

    submit = SubmitField(
        "Guardar", render_kw={"class": "button-gradient"}
    )

    def validate_address(form, address_field):
        "Valida la dirección del formulario"

        if not address_field.validate(form):
            return None

        id_meeting_point = form.id.data

        if id_meeting_point:
            meeting_point = MeetingPoint.find_by_id(
                id_meeting_point
            )
            if not meeting_point:
                raise ValidationError(
                    "No se encontró el punto de encuentro que se desea modificar"
                )

            # la dirección que quiere cargar el usuario
            form_address = address_field.data.lower()

            if (
                MeetingPoint.exists_address(form_address)
                and form_address
                != meeting_point.address.lower()
            ):
                # quiere usar una dirección que ya existe
                raise ValidationError(
                    "Ya existe un punto de encuentro con esa dirección"
                )
        else:
            if MeetingPoint.exists_address(
                address_field.data
            ):
                raise ValidationError(
                    "Ya existe un punto de encuentro con esa dirección"
                )

    def validate_coordinate(form, coordinate_field):
        "Valida las coordenadas del formulario"

        (
            valid_coordinates,
            coordinate,
            errors,
        ) = validate_json_coordinate_list(
            coordinate_field.data, 1
        )

        if valid_coordinates:
            coordinate_field.data = coordinate[0]
        else:
            raise ValidationError(
                f"Por favor, corrija las coordenadas: {errors}"
            )

    def meeting_point_data(self):
        "Retorna los datos recolectados del punto de encuentro"

        data = self.data
        for i in ("submit", "csrf_token", "id"):
            del data[i]

        return data
