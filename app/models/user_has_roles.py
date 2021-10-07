# -*- coding: utf-8 -*-
from app.db import db


user_has_roles = db.Table(
    "user_has_roles",
    db.Column("role_id", db.ForeignKey("roles.id"), primary_key=True),
    db.Column(
        "user_id",
        db.ForeignKey("users.id"),
        primary_key=True,
    ),
)
