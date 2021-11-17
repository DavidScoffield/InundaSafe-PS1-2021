from wtforms import (
    SubmitField,
    validators,
    StringField,
    SelectField,
    HiddenField,
    TextAreaField,
    ValidationError
)
from flask_wtf import FlaskForm
from app.models.evacuation_route import EvacuationRoute
from app.helpers.validate_coordinates import validate_json_coordinate_list


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

    def validate_name(form, name_field):
        "Valida el nombre del formulario"

        if not name_field.validate(form):
            return None

        id_evacuation_route = form.id.data

        if (id_evacuation_route):
            evacuation_route = EvacuationRoute.find_by_id(id_evacuation_route)
            if not evacuation_route:
                raise ValidationError("No se encontró el recorrido de evacuación que se desea modificar")
            
            # el nombre que quiere cargar el usuario
            name_field = name_field.data.lower()

            if (EvacuationRoute.exists_name(name_field) and name_field != evacuation_route.name.lower()):
                # quiere usar un nombre que ya existe
                raise ValidationError("Ya existe un recorrido de evacuación con ese nombre")
        else:
            if EvacuationRoute.exists_name(name_field.data):
                raise ValidationError("Ya existe un recorrido de evacuación con ese nombre")

    def validate_coordinates(form, coordinate_field):
        "Valida las coordenadas del formulario"

        valid_coordinates, coordinates, errors = validate_json_coordinate_list(coordinate_field.data, 3)

        if valid_coordinates:
            coordinate_field.data = coordinates
        else:
            raise ValidationError(f"Por favor, corrija las coordenadas: {errors}")

    def evacuation_route_data(self):
        "Retorna los datos recolectados del recorrido de evacuación"

        data = self.data
        for i in ("submit", "csrf_token", "id"):
            del data[i]

        return data