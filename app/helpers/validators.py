from app.helpers.config import actual_config


def is_empty(string: str) -> bool:
    """Comprueba si el parametro pasado es vacio o no"""
    return string.strip() == ""


def validate_params_pagination(page):
    """
    Validacion de parametros para paginacion por API.

    Logica {
        Si no hay "page"
            - Establezco la pagina = 1
            - Limito hasta 200(para que servidor no se
            sobrecargue devolviendo datos) elem por pagina

        Si hay "page"
            - Validar que el dato entrante sea entero
            - Establecer el valor "per_page" con la config del sistema
    }
    """

    if page is None:
        page = 1
        per_page = 200
    else:
        page = int(page)
        per_page = actual_config().elements_quantity

    return (page, per_page)


def validate_received_params(params):
    """
    Valida que los nombres de los parametros sean los correctos
    """

    valids_params = ["pagina"]

    if len(params.getlist("pagina")) > 1:
        return False

    params = list(params.keys())

    for param in params:
        if param not in valids_params:
            return False

    return True
