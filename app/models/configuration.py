# -*- coding: utf-8 -*-
from app.db import db


class Configuration(db.Model):

    __tablename__ = "configuration"
    id = db.Column(db.Integer, primary_key=True)
    elements_quantity = db.Column(db.Integer, nullable=False, default=50)
    order_by = db.Column(db.String(25), nullable=False, default="asc")
    colors_id_public = db.Column(
        db.Integer, db.ForeignKey("colors.id"), nullable=False, default="asc"
    )
    colors_public = db.relationship("Color", foreign_keys=[colors_id_public])
    colors_id_private = db.Column(
        db.Integer, db.ForeignKey("colors.id"), nullable=False, default="asc"
    )
    colors_private = db.relationship("Color", foreign_keys=[colors_id_private])

    def __repr__(self):
        return "<Configuration %r>" % self.id

    def __init__(
        self,
        elements_quantity: int = None,
        order_by: str = None,
        colors_id_public: int = None,
        colors_id_private: int = None,
    ):
        self.elements_quantity = elements_quantity
        self.order_by = order_by
        self.colors_id_public = colors_id_public
        self.colors_id_private = colors_id_private

    @classmethod
    def actual(cls):
        return Configuration.query.all()[0]
