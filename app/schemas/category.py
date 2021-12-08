from marshmallow import Schema, fields

class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str(data_key="nombre")

categories_schema = CategorySchema(
    many=True,
)