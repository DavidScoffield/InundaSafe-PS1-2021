from marshmallow import Schema, fields
from app.schemas.coordinate import coordinate_schema


class EvacuationRouteSchema(Schema):
    id = fields.Int()
    state = fields.Str()
    name = fields.Str(data_key="nombre")
    description = fields.Str(data_key="descripcion")
    coordinates = fields.Nested(
        coordinate_schema, many=True, data_key="coordenadas"
    )


evacuation_route_schema = EvacuationRouteSchema(
    only=("id", "name", "description", "coordinates")
)

evacuation_routes_schema = EvacuationRouteSchema(
    only=("id", "name", "description", "coordinates"),
    many=True,
)


class EvacuationRoutePaginateSchema(Schema):
    total = fields.Int()
    page = fields.Int(data_key="pagina")
    pages = fields.Int(data_key="paginas")
    per_page = fields.Int(data_key="por_pagina")
    items = fields.Nested(
        evacuation_route_schema,
        many=True,
        data_key="recorridos",
    )


evacuation_routes_paginated_schema = (
    EvacuationRoutePaginateSchema()
)
