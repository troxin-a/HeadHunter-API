from pytest import fixture

from src.classes.vacancy import Vacancy


@fixture
def vacancy_1():
    return Vacancy("Вакансия 1", "", {'from': 50, 'to': 100}, "")


@fixture
def vacancy_2():
    return Vacancy("Вакансия 2", "", {'from': 50, 'to': 100}, "")
