from marshmallow import Schema, fields
from app.schemas.coordinate import coordinate_schema


class MeetingPointSchema(Schema):
    id = fields.Int()
    name = fields.Str(data_key="nombre")
    state = fields.Str()
    address = fields.Str(data_key="direccion")
    email = fields.Str()
    telephone = fields.Str(data_key="telefono")
    coordinate = fields.Nested(
        coordinate_schema, data_key="coordenada"
    )


meeting_point_schema = MeetingPointSchema(
    only=(
        "id",
        "name",
        "address",
        "email",
        "telephone",
        "coordinate",
    )
)

meeting_points_schema = MeetingPointSchema(
    only=(
        "id",
        "name",
        "address",
        "email",
        "telephone",
        "coordinate",
    ),
    many=True,
)


class MeetingPointPaginateSchema(Schema):
    total = fields.Int()
    page = fields.Int(data_key="pagina")
    pages = fields.Int(data_key="paginas")
    per_page = fields.Int(data_key="por_pagina")
    items = fields.Nested(
        meeting_point_schema,
        many=True,
        data_key="puntos_encuentro",
    )


meeting_points_paginated_schema = (
    MeetingPointPaginateSchema()
)
