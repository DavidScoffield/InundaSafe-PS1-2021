from marshmallow import Schema, fields, post_dump
from app.schemas.coordinate import coordinate_schema
from app.helpers.logger import logger_info


class FloodZoneSchema(Schema):
    id = fields.Int()
    cipher = fields.Str(data_key="codigo")
    state = fields.Str(data_key="estado")
    name = fields.Str(data_key="nombre")
    color = fields.Str()
    coordinates = fields.Nested(
        coordinate_schema, many=True, data_key="coordenadas"
    )

    @post_dump
    def format_dump(self, data, **kwargs):
        "Formatea el dump del schema. En especifico el estado de ingles -> español"

        data["estado"] = (
            "publicado"
            if data["estado"] == "publicated"
            else "despublicado"
        )

        return data


flood_zone_schema = FloodZoneSchema(
    only=(
        "id",
        "name",
        "color",
        "coordinates",
        "state",
        "cipher",
    )
)

flood_zones_schema = FloodZoneSchema(
    only=("id", "name", "color", "coordinates"), many=True
)


class FloodZonePaginateSchema(Schema):
    total = fields.Int()
    page = fields.Int(data_key="pagina")
    pages = fields.Int(data_key="paginas")
    per_page = fields.Int(data_key="por_pagina")
    items = fields.Nested(
        flood_zone_schema,
        many=True,
        data_key="zonas",
    )


flood_zones_paginate_schema = FloodZonePaginateSchema()
