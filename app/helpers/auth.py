def authenticated(session):
    "Retorna el id de usuario almacenado en la session en caso de existir"
    return session.get("user")
