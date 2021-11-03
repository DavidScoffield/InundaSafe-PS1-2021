import re

def validate_coordinates(coordinates):
    """"Verifica si el formato de la coordenada es válido.

        'coordinates': lista que contiene la latitud y longitud"""

    for coordinate in coordinates:
        if not re.fullmatch("^-?[0-9]{1,100}(\.[0-9]+)?$", str(coordinate)):
            return False
    
    return True