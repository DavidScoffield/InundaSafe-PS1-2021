def check_param(param_name, param):
    """
    Formatea el parametro pasado dependiendo cual es y de que modelo
    Recibe:
     - param_name : string -> valor para recuperar la posicion del diccionario especifica
     - param : string -> parametro a evaluar

    """
    return {
        "@meeting_point/name": param
        if param is not None
        else "",
        "@meeting_point/state": param
        if param != "all" and param is not None
        else "",
        "@flood_zones/name": param
        if param is not None
        else "",
        "@flood_zones/state": param
        if param != "all" and param is not None
        else "",
        "@user/name": param if param is not None else "",
        "@user/active": param
        if type(param) is int and param is not None
        else "",
    }.get(param_name)


def active_dic(state):
    """Formatea el parametro state para trabajar correctamente con el modelo"""
    return {
        "publicated": 1,
        "despublicated": 0,
        "all": None,
    }.get(state)
