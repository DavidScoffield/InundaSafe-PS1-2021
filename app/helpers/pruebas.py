from app.models.models import Color, MeetingPoint, Permission, Role, User, Configuration


def modelsTest():
    print("------> MODELS TEST")
    out = Configuration.query.all()
    print("------------------------PRINT--------------------")
    print(out[0].colors_public.color_1)
    # print(out)
    print("------------------------PRINT--------------------")
