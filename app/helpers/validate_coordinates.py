import json
import re


def validate_coordinates(coordinates):
    """
    Verifica si el formato de la coordenada es válido.

    'coordinates': lista que contiene la latitud y longitud
    """

    #! TODO: Chequear porque el regex no funciona del todo bien

    for coordinate in coordinates:
        if not re.fullmatch(
            "^-?[0-9]{1,100}(\.[0-9]+)?$", str(coordinate)
        ):
            return False

    return True


def coordinates_encode(coordinates: list):
    return json.dumps(
        [coor.as_array() for coor in coordinates]
    )
