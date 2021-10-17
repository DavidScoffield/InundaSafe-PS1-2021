# -*- coding: utf-8 -*-
from app.db import db


class Configuration(db.Model):
    """Modelo para el manejo de la tabla Configuration de la base de datos"""

    __tablename__ = "configuration"
    id = db.Column(db.Integer, primary_key=True)
    elements_quantity = db.Column(
        db.Integer, nullable=False, default=50
    )
    order_by = db.Column(
        db.String(25), nullable=False, default="asc"
    )
    colors_id_public = db.Column(
        db.Integer,
        db.ForeignKey("colors.id"),
        nullable=False,
        default="asc",
    )
    colors_public = db.relationship(
        "Color", foreign_keys=[colors_id_public]
    )
    colors_id_private = db.Column(
        db.Integer,
        db.ForeignKey("colors.id"),
        nullable=False,
        default="asc",
    )
    colors_private = db.relationship(
        "Color", foreign_keys=[colors_id_private]
    )

    def __repr__(self):
        return "<Configuration %r>" % self.id

    def __init__(
        self,
        elements_quantity: int = None,
        order_by: str = None,
        colors_id_public: int = None,
        colors_id_private: int = None,
    ):
        """Contructor del modelo"""
        self.elements_quantity = elements_quantity
        self.order_by = order_by
        self.colors_id_public = colors_id_public
        self.colors_id_private = colors_id_private

    @classmethod
    def actual(cls):
        """Obtiene la configuracion actual de la base de datos"""
        return Configuration.query.limit(1).all()[0]

    @classmethod
    def update(
        cls,
        elements_quantity: int = None,
        order_by: str = None,
        colors_id_public: int = None,
        colors_id_private: int = None,
    ):
        """Actualiza la configuracion del sistema con los parametros pasajos en el metodo"""
        actual = Configuration.actual()
        actual.elements_quantity = elements_quantity
        actual.order_by = order_by
        actual.colors_id_public = colors_id_public
        actual.colors_id_private = colors_id_private
        db.session.commit()
