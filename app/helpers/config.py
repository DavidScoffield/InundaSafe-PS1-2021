from app.models.configuration import Configuration


def actual_config():
    return Configuration.actual()
