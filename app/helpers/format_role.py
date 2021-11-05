def format_role(role):
    """Formatea el parametro role para renderizarlo bonito en el listado de usuarios"""
    return {
        "rol_administrador": "Administrador",
        "rol_operador": "Operador",
    }.get(role)