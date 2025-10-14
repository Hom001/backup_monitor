import json
from typing import Union, Dict, List


def read_json(filename: str) -> Union[List[str], Dict[str, List]]:
    """
    Универсальная читалка JSON-файлов с обработкой ошибок.

    :param filename: путь к файлу
    :return: список или словарь из JSON
    :raises: FileNotFoundError, json.JSONDecodeError
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f'Файл не найден: {filename}')
    except json.JSONDecodeError as e:
        raise ValueError(f'Ошибка при чтении JSON из файла {filename}: {e}')