from app.models.configuration import Configuration


def actual_config():
    """Retorna la configuracion actual almancenada en la base de datos"""
    return Configuration.actual()
