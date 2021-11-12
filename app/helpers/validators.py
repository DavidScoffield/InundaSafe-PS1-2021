from app.helpers.config import actual_config


def is_empty(string: str) -> bool:
    """Comprueba si el parametro pasado es vacio o no"""
    return string.strip() == ""


def validate_params_pagination(page, per_page):
    """
    Validacion de parametros para paginacion por API.

    Logica para "per_page"{
        Si no hay "per_page"
            Si "page" == 1
                limito hasta 200(servidor no se sobrecargue devolviendo datos)
            sino
                establezco el valor dado por la config del sistema
        Si hay per_page
            validar que el dato entrante sea entero
    }

    """

    if per_page is None:
        if page == 1:
            per_page = 200
        else:
            per_page = actual_config().elements_quantity
    else:
        per_page = int(per_page)

    return (page, per_page)
