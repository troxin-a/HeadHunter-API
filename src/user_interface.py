from math import ceil

from connect_api import ConnectAPI
from vacancy import Vacancy, CompareMethodMinSalary, CompareMethodMaxSalary


def download_vacancies(text: str, quantity: int):
    api = ConnectAPI()

    if quantity > 2000:
        quantity = 2000
    pages = ceil(abs(quantity) / 20)

    data = []
    for page in range(pages):
        items = api.connect(f"https://api.hh.ru/vacancies?area=113&text={text}&page={page}")
        data.extend(items)
        download_progress = round(100 / (pages / (page + 1)))
        print(f"Загружено {download_progress}%")
    print("Загрузка завершена")

    return data


def create_obj_vacancies_from_hhru(data: list, quantity: int = None) -> list:
    objects = []
    for vacancy in data:
        name = vacancy.get("name")
        city = vacancy.get("area").get("name")
        url = vacancy.get("alternate_url")
        salary = vacancy.get("salary")
        requirements = vacancy.get("snippet").get("requirement")
        objects.append(Vacancy(name, city, url, salary, requirements))
    if quantity:
        return objects[:quantity]
    return objects


def create_obj_vacancies_from_file(data: list, quantity: int = None) -> list:
    objects = []
    for vacancy in data:
        name = vacancy.get("name")
        city = vacancy.get("city")
        url = vacancy.get("url")
        salary = vacancy.get("_salary")
        requirements = vacancy.get("requirements")
        objects.append(Vacancy(name, city, url, salary, requirements))
    if quantity:
        return objects[:quantity]
    return objects


def sort_method():
    method = None
    while method not in ["1", "2"]:
        method = input("Чтобы отсортировать по наименьшей з/п, введите 1, по наибольшей - 2: ")
        if method == "1":
            Vacancy.set_compare_method(CompareMethodMinSalary())
        elif method == "2":
            Vacancy.set_compare_method(CompareMethodMaxSalary())
        else:
            print("Только 1 или 2")
            continue
        break
