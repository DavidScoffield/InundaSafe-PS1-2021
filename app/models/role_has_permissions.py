# -*- coding: utf-8 -*-
from app.db import db


role_has_permissions = db.Table(
    "role_has_permissions",
    db.Column(
        "role_id",
        db.ForeignKey("roles.id"),
        primary_key=True,
    ),
    db.Column(
        "permission_id",
        db.ForeignKey("permissions.id"),
        primary_key=True,
    ),
)
