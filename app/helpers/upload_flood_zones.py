import csv
import json
import os
from werkzeug.utils import secure_filename
from app.helpers.logger import logger_info
from app.helpers.validate_coordinates import (
    validate_coordinates as validate_coor,
)

from app.models.flood_zones import FloodZones


ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename: str):
    """
    Comprueba que el nombre de archivo pasado pertenezca al grupo de extensiones permitidas
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def read_file(filePath: str):
    """
    Lee el archivo ubicado en `filePath` y lo transforma.
    -> Devuelve:
        - file_data: una lista de diccionarios con los datos del archivo.
        - error_data: una lista con los datos que no pudieron procesarse del archivo.
    """
    with open(filePath, mode="r") as csv_file:
        csv_reader = csv.DictReader(
            csv_file,
            delimiter=",",
            # fieldnames=["name", "area"],
        )

        # file_data = list(map(convert_row, list(csv_reader)))
        file_data = []
        error_data = []
        for row in list(csv_reader):
            try:
                file_data.append(convert_row(row))
            except:
                error_data.append(row)

        return (file_data, error_data)


def convert_row(row: dict):
    """
    Deserealiza el `area` de la columna pasada por parametro
    row : dict
    """
    row["area"] = string_to_list(row["area"])
    return row


def string_to_list(string: str):
    """Convierte el string pasado en una lista"""
    return json.loads(string)


# Persisting files in filesystem
def save_file_filesystem(file, current_app):
    """
    Guarda el archivo pasado en la carpeta predeterminada para esto
    """
    filename = secure_filename(file.filename)

    file_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename,
    )
    file.save(file_path)

    return file_path


def remove_file_filesystem(file_path):
    """
    Elimina el archivo pasado por parametro
    file_path : str -> espera la direccion en el filesystem del archivo
    """
    os.remove(file_path)


# Persisting data in BD
def save_data(data: list):
    """
    Guarda los datos de las zonas inundables en `data` en la BD.
    -> Actializa en caso de que ya exista
    -> Crea una nueva de no existir
    """
    for item in data:
        flood_zone = FloodZones.find_by_name(item["name"])
        if flood_zone:
            flood_zone.update(coordinates=item["area"])
        else:
            FloodZones.new(
                name=item["name"], coordinates=item["area"]
            )


# Validations
def validate_data(data: list, error: list):
    """
    Valida los campos en los datos de `data`, en caso que alguno no cumple,
    los saca de `data` y los guarda en `error`
    """
    # TODO: Validar que posee el campo Title obligatorio. Y asi para los demas
    validated_data = list()
    for item in data:
        if len(
            item["area"]
        ) < 3 or not validate_coordinates(item["area"]):
            error.append(item)
        else:
            validated_data.append(item)

    return (validated_data, error)


def validate_coordinates(list_coordinates: list):
    """
    Valida que le llegue una lista de pares de coordenadas.
    Comprueba que todos las coordenadas de la lista de pares de coordenadas
    posean un formato válido.
    """
    for peer_coordinates in list_coordinates:
        if (
            type(peer_coordinates) is not list
            or len(peer_coordinates) != 2
            or not validate_coor(peer_coordinates)
        ):
            return False
    return True
