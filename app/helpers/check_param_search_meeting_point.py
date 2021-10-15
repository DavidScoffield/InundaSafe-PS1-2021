def check_param(param_name, param):
    return {
        "state": param
        if param != "all" and param is not None
        else "",
        "name": param if param is not None else "",
    }.get(param_name)
