from pytest import fixture

from src.connect_api import ConnectAPI
from src.db_connector import DBConnector
from src.vacancy import Vacancy, CompareMethodMinSalary, CompareMethodMaxSalary


@fixture
def vacancy_1():
    return Vacancy("Вакансия 1", "Красноярск", "1", {'from': 50, 'to': 100}, "")


@fixture
def vacancy_2():
    return Vacancy("Вакансия 2", "Красноярск", "2", {'from': 50, 'to': 100}, "")


@fixture
def compare_method_min():
    return CompareMethodMinSalary()


@fixture
def compare_method_max():
    return CompareMethodMaxSalary()


@fixture
def db_connector():
    return DBConnector("test.json")


@fixture
def my_data():
    return [
        {"a": "Москва", "y": "Профессия"},
        {"a": "Москва Красноярск", "y": "Профессия"},
        {"a": "Красноярск", "y": "Профессия"},
        {"a": "Красноярск", "y": "Ничего"},
    ]


@fixture
def dict_from_hhru():
    vacancy = {
        "name": "Питон",
        "area": {"name": "Москва"},
        "alternate_url": "url-адрес",
        "salary": {"from": 10, "to": 20},
        "snippet": {"requirement": "Работать"}
    }
    return vacancy


@fixture
def dict_from_file():
    vacancy = {
        "name": "Питон",
        "city": "Москва",
        "url": "url-адрес",
        "_salary": [10, 20],
        "requirements": "Работать"
    }
    return vacancy


@fixture
def data_from_file():
    vacancies = [
        {
            "name": "Питон",
            "city": "Москва",
            "url": "url-адрес",
            "_salary": [10, 20],
            "requirements": "Работать"
        },
        {
            "name": "Крановщик",
            "city": "Тура",
            "url": "url-адрес",
            "_salary": [15, 30],
            "requirements": "Работать надо"
        }
    ]
    return vacancies


@fixture
def api_obj():
    return ConnectAPI()
