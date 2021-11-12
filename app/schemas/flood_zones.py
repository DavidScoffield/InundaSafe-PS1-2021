from marshmallow import Schema, fields
from app.schemas.coordinate import coordinate_schema


class FloodZoneSchema(Schema):
    id = fields.Int()
    cipher = fields.Str()
    state = fields.Str()
    name = fields.Str(data_key="nombre")
    color = fields.Str()
    coordinates = fields.Nested(
        coordinate_schema, many=True, data_key="coordenadas"
    )


flood_zone_schema = FloodZoneSchema(
    only=("id", "name", "color", "coordinates")
)

flood_zones_schema = FloodZoneSchema(
    only=("id", "name", "color", "coordinates")
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
