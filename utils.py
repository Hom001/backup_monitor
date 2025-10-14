import json
from typing import Union, Dict, List


def read_json_list(filename: str) -> List[str]:
    """
    Универсальная читалка JSON-файлов с обработкой ошибок.

    :param filename: путь к файлу
    :return: список или словарь из JSON
    :raises: FileNotFoundError, json.JSONDecodeError
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError(f'{filename} должен содержать список.')
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f'Файл не найден: {filename}')
    except json.JSONDecodeError as e:
        raise ValueError(f'Ошибка при чтении JSON из файла {filename}: {e}')