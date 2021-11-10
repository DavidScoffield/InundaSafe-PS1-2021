import json
import re

def validate_coordinates(coordinates):
    """
    Verifica si el formato de la coordenada es válido.

    'coordinates': lista que contiene la latitud y longitud de la coordenada.
    """

    for coordinate in coordinates:
        if not re.fullmatch(
            "^-?[0-9]{1,100}(\.[0-9]+)?$", str(coordinate)
        ):
            return False

    return True


def validate_json_coordinate_list(json_coordinate_list):
    """
    Verifica que el listado de coordenadas en formato json sea válido.

    'json_coordinate_list': listado de coordenadas en formato json.

    Retorna si el listado es válido o no, la lista de coordenadas y los errores en caso de que haya alguno.
    """

    valid_coordinates = True
    coordinates = []
    errors = ""
            
    try:
        coordinates = json.loads(json_coordinate_list)
    except:
        errors += "Ocurrió un error al procesar las coordenadas, por favor, inténtelo de nuevo. "
        valid_coordinates = False

    if (len(coordinates) < 3):
        errors += "El recorrido de evacuación debe contener al menos 3 puntos. "
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
