import pytest

from src.classes.vacancy import Vacancy, CompareMethodMinSalary, CompareMethodMaxSalary


def test_str(vacancy_1, capsys):
    print(vacancy_1)
    out, err = capsys.readouterr()
    assert out == 'Вакансия 1. Зарплата: от 50 до 100\n'
    assert err == ''

    vacancy_1.salary = {'from': None, 'to': 10}
    print(vacancy_1)
    out, err = capsys.readouterr()
    assert out == 'Вакансия 1. Зарплата: до 10\n'
    assert err == ''

    vacancy_1.salary = {'from': 10, 'to': None}
    print(vacancy_1)
    out, err = capsys.readouterr()
    assert out == 'Вакансия 1. Зарплата: от 10\n'
    assert err == ''

    vacancy_1.salary = None
    print(vacancy_1)
    out, err = capsys.readouterr()
    assert out == 'Вакансия 1. Зарплата: не указана\n'
    assert err == ''


def test_salary_setter(vacancy_1):
    vacancy_1.salary = None
    assert vacancy_1.salary == (0, 0)
    vacancy_1.salary = {'from': None, 'to': 10}
    assert vacancy_1.salary == (0, 10)
    vacancy_1.salary = {'from': 10, 'to': None}
    assert vacancy_1.salary == (10, 0)
    vacancy_1.salary = {'to': 20}
    assert vacancy_1.salary == (0, 20)


def test_salary_setter_wrong_type(vacancy_1):
    with pytest.raises(TypeError):
        vacancy_1.salary = 10


def test_eq_wrong_type(vacancy_1):
    with pytest.raises(TypeError):
        vacancy_1 == 1


def test_le_wrong_type(vacancy_1):
    with pytest.raises(TypeError):
        vacancy_1 <= 1


def test_lt_wrong_type(vacancy_1):
    with pytest.raises(TypeError):
        vacancy_1 < 1


def test_compare_eq_min(vacancy_1, vacancy_2):
    Vacancy.compare_method = CompareMethodMinSalary
    assert vacancy_1 == vacancy_2

    vacancy_1.salary = {'from': None, 'to': 100}
    assert vacancy_1 != vacancy_2


def test_compare_le_min(vacancy_1, vacancy_2):
    Vacancy.compare_method = CompareMethodMinSalary
    assert vacancy_1 <= vacancy_2
    assert vacancy_1 >= vacancy_2

    vacancy_1.salary = {'from': None, 'to': 100}
    assert vacancy_1 <= vacancy_2

    vacancy_1.salary = None
    assert vacancy_2 >= vacancy_1


def test_compare_lt_min(vacancy_1, vacancy_2):
    Vacancy.compare_method = CompareMethodMinSalary

    vacancy_1.salary = {'from': 30, 'to': 100}
    assert vacancy_1 < vacancy_2
    assert vacancy_2 > vacancy_1


def test_compare_eq_max(vacancy_1, vacancy_2):
    Vacancy.compare_method = CompareMethodMaxSalary
    assert vacancy_1 == vacancy_2

    vacancy_1.salary = {'from': 50, 'to': None}
    assert vacancy_1 != vacancy_2


def test_compare_le_max(vacancy_1, vacancy_2):
    Vacancy.compare_method = CompareMethodMaxSalary
    assert vacancy_1 <= vacancy_2
    assert vacancy_1 >= vacancy_2

    vacancy_1.salary = {'from': 50, 'to': None}
    assert vacancy_1 <= vacancy_2
    assert vacancy_2 >= vacancy_1

    vacancy_1.salary = None
    assert vacancy_1 <= vacancy_2


def test_compare_lt_max(vacancy_1, vacancy_2):
    Vacancy.compare_method = CompareMethodMaxSalary

    vacancy_1.salary = {'from': 50, 'to': 90}
    assert vacancy_1 < vacancy_2
    assert vacancy_2 > vacancy_1
