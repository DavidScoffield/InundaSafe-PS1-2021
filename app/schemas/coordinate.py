from marshmallow import Schema, fields


class CoordinateSchema(Schema):
    id = fields.Int()
    latitude = fields.Str(data_key="lat")
    longitude = fields.Str(data_key="long")


coordinate_schema = CoordinateSchema(
    only=("latitude", "longitude")
)
coordinates_schema = CoordinateSchema(
    many=True, only=("latitude", "longitude")
)
