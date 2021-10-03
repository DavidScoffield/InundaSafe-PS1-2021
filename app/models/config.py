# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Config(db.Model):

    __tablename__ = "config"
    id = db.Column(db.Integer, primary_key=True)
    elements_quantity = db.Column(db.Integer, nullable=False, default=50)
    order_by = db.Column(db.String(25), nullable=False, default='asc')
    colors_id = db.Column(db.Integer, nullable=False, default='asc')

    def __repr__(self):
        return '<Config %r>' % self.name
