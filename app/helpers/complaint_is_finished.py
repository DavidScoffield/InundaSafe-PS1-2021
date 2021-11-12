finished_states = ["Resuelta", "Cerrada"]

def complaint_is_finished(complaint):
    """Devuelve True si la Denuncia que llega por parametro esta en estado 'Resuelta' o 'Cerrada'"""
    return complaint.state in finished_states