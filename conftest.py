from pytest import fixture

from src.classes.db_connector import DBConnector
from src.classes.vacancy import Vacancy, CompareMethodMinSalary, CompareMethodMaxSalary


@fixture
def vacancy_1():
    return Vacancy("Вакансия 1", "Красноярск", "1", {'from': 50, 'to': 100}, "")


@fixture
def vacancy_2():
    return Vacancy("Вакансия 2", "Красноярск", "2", {'from': 50, 'to': 100}, "")


@fixture
def vacancy_list():
    lst = [
        Vacancy("Вакансия 1", "Красноярск", "3", {'from': 200, 'to': 300}, ""),
        Vacancy("Вакансия 2", "Москва", "4", {'from': 10, 'to': 50}, ""),
        Vacancy("Вакансия 3", "С. Петербург", "5", {'from': 30, 'to': 80}, ""),
        Vacancy("Вакансия 4", "Красноярск", "6", {'from': 40, 'to': 600}, ""),
        Vacancy("Вакансия 5", "Красноярск", "7", {'from': 300, 'to': 500}, ""),
    ]
    return lst


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
        {"a": "c", "y": 2},
        {"a": "c", "y": 6},
        {"a": "d", "y": 6},
        {"a": "d", "y": 2}
    ]
