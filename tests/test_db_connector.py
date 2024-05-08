from os import remove, path
import json

from src.db_connector import DBConnector
from config import ROOT_DIR


def test_read_no_file():
    db_connector = DBConnector("to_remove.json")
    db_connector.file_json = path.join(ROOT_DIR, "tests", "to_remove.json")
    assert db_connector.read() == []
    remove(db_connector.file_json)


def test_read_empty_file():
    db_connector = DBConnector("empty.json")
    db_connector.file_json = path.join(ROOT_DIR, "tests", "empty.json")
    assert db_connector.read() == []
    with open(db_connector.file_json, "w", encoding="UTF-8") as file:
        file.write("")


def test_read_file(db_connector):
    db_connector.file_json = path.join(ROOT_DIR, "tests", "test.json")
    with open(db_connector.file_json, "w", encoding="UTF-8") as file:
        file.write("")
    assert db_connector.read() == []


def test_add_vacancy(db_connector, vacancy_1, vacancy_2):
    db_connector.file_json = path.join(ROOT_DIR, "tests", "test.json")
    with open(db_connector.file_json, "w", encoding="UTF-8") as file:
        file.write("")

    db_connector.add_vacancy(vacancy_1)
    assert db_connector.read() == [
        {'name': 'Вакансия 1', 'city': 'Красноярск', 'url': '1', '_salary': [50, 100], 'requirements': ''}
    ]

    db_connector.add_vacancy(vacancy_2)
    assert db_connector.read() == [
        {'name': 'Вакансия 1', 'city': 'Красноярск', 'url': '1', '_salary': [50, 100], 'requirements': ''},
        {'name': 'Вакансия 2', 'city': 'Красноярск', 'url': '2', '_salary': [50, 100], 'requirements': ''}
    ]


def test_delete_vacancy(db_connector, vacancy_1, vacancy_2):
    db_connector.file_json = path.join(ROOT_DIR, "tests", "test.json")
    with open(db_connector.file_json, "w", encoding="UTF-8") as file:
        file.write("")

    db_connector.add_vacancy(vacancy_1)
    db_connector.add_vacancy(vacancy_2)
    db_connector.delete_vacancy(vacancy_2)
    assert db_connector.read() == [
        {'name': 'Вакансия 1', 'city': 'Красноярск', 'url': '1', '_salary': [50, 100], 'requirements': ''},
    ]


def test_get_vacancies(db_connector, my_data):
    db_connector.file_json = path.join(ROOT_DIR, "tests", "test.json")
    with open(db_connector.file_json, "w", encoding="UTF-8") as file:
        data = json.dumps(my_data)
        file.write(data)
    selections = {}
    assert db_connector.get_vacancies(selections) == my_data

    selections = ["москва"]
    assert db_connector.get_vacancies(selections) == [{"a": "Москва", "y": "Профессия"},
                                                      {"a": "Москва Красноярск", "y": "Профессия"}
                                                      ]

    selections = ["красноярск", "профессия"]
    assert db_connector.get_vacancies(selections) == [{"a": "Москва Красноярск", "y": "Профессия"},
                                                      {"a": "Красноярск", "y": "Профессия"},
                                                      ]
