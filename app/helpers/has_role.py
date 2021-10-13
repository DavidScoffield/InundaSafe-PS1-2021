def has_role(roles, rol_to_check):
    """Llega una lista de roles, busca si el name de alguno es == rol_administrador"""
    for rol in roles:
        if rol.name == rol_to_check:
            return True
    return False