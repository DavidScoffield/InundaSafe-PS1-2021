def active_dic(state):
    """Formatea el parametro state para trabajar correctamente con WTF"""
    return {
        1: "activo",
        0: "bloqueado",
    }.get(state)