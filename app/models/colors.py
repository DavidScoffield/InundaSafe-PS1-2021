# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Color(db.Model):

    __tablename__ = "colors"
    id = db.Column(db.Integer, primary_key=True)
    color_1 = db.Column(db.String(15), nullable=False)
    color_2 = db.Column(db.String(15), nullable=False)
    color_3 = db.Column(db.String(15), nullable=False)
    color_4 = db.Column(db.String(15), nullable=False)
    color_5 = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return '<Color %r>' % self.name

    def __init__(self, color_1: str = None,color_2: str = None,color_3: str = None,color_4: str = None,color_5: str = None):
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.color_4 = color_4
        self.color_5 = color_5
