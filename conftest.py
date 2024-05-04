from pytest import fixture

from src.classes.vacancy import Vacancy, CompareMethodMinSalary, CompareMethodMaxSalary


@fixture
def vacancy_1():
    return Vacancy("Вакансия 1", "", {'from': 50, 'to': 100}, "")


@fixture
def vacancy_2():
    return Vacancy("Вакансия 2", "", {'from': 50, 'to': 100}, "")


@fixture
def compare_method_min():
    return CompareMethodMinSalary()

@fixture
def compare_method_max():
    return CompareMethodMaxSalary()
