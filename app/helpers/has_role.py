def has_role(roles, rol_to_check):
    """Chequea si rol_to_check esta dentro de roles"""
    for rol in roles:
        if rol.name == rol_to_check:
            return True
    return False
