# from app.models.models import Color, MeetingPoint, Permission, Role, User, Configuration
#

from app.models.permission import Permission
from app.models.role import Role
from app.models.colors import Color
from app.models.configuration import Configuration
from app.models.meeting_point import MeetingPoint
from app.models.user import User


def modelsTest():
    """Funcion para comprobar que todos los modelos definidos con SQLAlchemy funcionan correctamente"""
    print("------> MODELS TEST")
    print(
        "------------------------PERMISSION--------------------"
    )
    out = Permission.query.all()
    print(out[0].roles)
    # print(out)
    print(
        "------------------------------------------------------"
    )
    print(
        "------------------------ROLE--------------------"
    )
    out = Role.query.all()
    print(out[1].permissions)
    # print(out)
    print(
        "------------------------------------------------------"
    )
    print(
        "------------------------COLORS--------------------"
    )
    out = Color.query.all()
    print(out[0])
    # print(out)
    print(
        "------------------------------------------------------"
    )
    print(
        "------------------------CONFIGURATION--------------------"
    )
    out = Configuration.query.all()
    print(out[0])
    # print(out)
    print(
        "------------------------------------------------------"
    )
    print(
        "------------------------MEETING_POINT--------------------"
    )
    out = MeetingPoint.query.all()
    # print(out[])
    print(out)
    print(
        "------------------------------------------------------"
    )
    print(
        "------------------------USER--------------------"
    )
    out = User.query.all()
    # print(out[7].roles)
    print(out)
    print(
        "------------------------------------------------------"
    )
