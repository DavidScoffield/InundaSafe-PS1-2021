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
