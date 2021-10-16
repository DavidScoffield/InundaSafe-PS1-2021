def check_param(param_name, param):
    return {
        "@meeting_point/name": param
        if param is not None
        else "",
        "@meeting_point/state": param
        if param != "all" and param is not None
        else "",
        "@user/name": param if param is not None else "",
        "@user/active": param
        if type(param) is int and param is not None
        else "",
    }.get(param_name)


def active_dic(state):
    return {
        "publicated": 1,
        "despublicated": 0,
        "all": None,
    }.get(state)
