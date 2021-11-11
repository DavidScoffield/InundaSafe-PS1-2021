import json
import re


def validate_coordinates(coordinates):
    """
    Verifica si el formato de la coordenada es válido.

    'coordinates': lista que contiene la latitud y longitud
    """

    for coordinate in coordinates:
        if not re.fullmatch(
            "^-?[0-9]{1,100}(\.[0-9]+)?$", str(coordinate)
        ):
            return False

    return True


def validate_json_coordinate_list(json_coordinate_list, points_needed = 3):
    """
    Verifica que el listado de coordenadas en formato json sea válido.

    'json_coordinate_list': listado de coordenadas en formato json.

    'points_needed': cantidad de puntos que se requieren (1 para puntos de encuentro y al menos 3 para recorridos de evacuación)

    Retorna si el listado es válido o no, la lista de coordenadas y los errores en caso de que haya alguno.
    """

    valid_coordinates = True
    coordinates = []
    errors = ""
    
    try:
        coordinates = json.loads(json_coordinate_list)
    except:
        errors += "Ocurrió un error al procesar las coordenadas, por favor, inténtelo de nuevo. "
        return False, coordinates, errors

    if (len(coordinates) < points_needed):
        errors += f"Por favor, seleccione al menos {points_needed} punto(s). "
        valid_coordinates = False

    for coordinate in coordinates:
        if not validate_coordinates(coordinate):
            errors += "Se ingresó una coordenada inválida"
            valid_coordinates = False
    
    return valid_coordinates, coordinates, errors


def coordinates_encode(coordinates: list):
    return json.dumps(
        [coor.as_array() for coor in coordinates]
    )
