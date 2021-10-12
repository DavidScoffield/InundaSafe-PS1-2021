def is_admin(roles):
    """Llega una lista de roles, busca si el name de alguno es == rol_administrador"""
    for rol in roles:
        if rol.name == "rol_administrador":
            return True
    return False