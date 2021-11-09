from app.db import db


class Category(db.Model):
    """Modelo para el manejo de la tabla Categoria de la base de datos"""

    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<Category %r>" % self.name

    def __init__(self, name: str = None):
        """Constructor del modelo"""
        self.name = name


    @classmethod
    def find_all_categories(cls):
        return Category.query.all()