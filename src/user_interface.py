from src.connect_api import ConnectAPI
from src.db_connector import DBConnector
from src.vacancy import Vacancy, CompareMethodMinSalary, CompareMethodMaxSalary


def create_obj_vacancies_from_hhru(data: list) -> list:
    """
    Функция создает список объектов класса Vacancy и возвращает его.
    Принимает json, загруженный с hh.ru и необходимое количество вакансий.
    """

    objects = []
    for vacancy in data:
        name = vacancy.get("name")
        city = vacancy.get("area").get("name")
        url = vacancy.get("alternate_url")
        salary = vacancy.get("salary")
        requirements = vacancy.get("snippet").get("requirement")
        objects.append(Vacancy(name, city, url, salary, requirements))
    return objects


def create_obj_vacancies_from_file(data: list) -> list:
    """
    Функция создает список объектов класса Vacancy и возвращает его.
    Принимает чистый json с локальной директории необходимое количество вакансий.
    """

    objects = []
    for vacancy in data:
        name = vacancy.get("name")
        city = vacancy.get("city")
        url = vacancy.get("url")
        salary = vacancy.get("_salary")
        requirements = vacancy.get("requirements")
        objects.append(Vacancy(name, city, url, salary, requirements))
    return objects


def filter_vacancies(db_connector: DBConnector):
    """
    Функция вызывает методы фильтрации и сортировки.
    Выводит итоговую таблицу на экран.
    Принимает объект класса DBConnector
    """

    print()
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    sort_method()
    filtered_vacancies = db_connector.get_vacancies(filter_words)
    vacancies = create_obj_vacancies_from_file(filtered_vacancies)
    vacancies.sort(reverse=True)
    print_table(vacancies)


def new_base(db_connector: DBConnector):
    """
    Функция запускает метод загрузки вакансий (по наименованию) в файл
    """

    to_del = db_connector.get_vacancies([])
    to_del = create_obj_vacancies_from_file(to_del)
    for vac in to_del:
        db_connector.delete_vacancy(vac)
    del to_del

    find_text = input("\nВведите название вакансии: ")
    quantity_vac = input("Сколько вакансий загрузить? До 2000: ")

    try:
        quantity_vac = int(quantity_vac)
    except ValueError:
        print("Количество должно быть числом")
        exit()

    api = ConnectAPI()
    vacancies_data = api.get_vacancies_data(find_text, quantity_vac)
    vacancies = create_obj_vacancies_from_hhru(vacancies_data)

    print("Сохраняю вакансии в файл...")
    for vacancy in vacancies:
        db_connector.add_vacancy(vacancy)
    print("Вакансии сохранены")

    filter_vacancies(db_connector)


def change_start(db_connector: DBConnector):
    """
    Функция с диалогом: начать работу с имеющейся базой или загрузить все заново
    """

    method = None
    while method not in ["1", "2"]:
        print("\n1. Загрузить вакансии с hh.ru")
        print("2. Воспользоваться имеющейся базой")
        method = input("Поле ввода: ")
        if method == "1":
            new_base(db_connector)
        elif method == "2":
            filter_vacancies(db_connector)
        else:
            print("Только 1 или 2")
            continue


def sort_method():
    """
    Функция с диалогом: определяет метод сортировки для вакансий
    """
    method = None
    while method not in ["1", "2"]:
        print("\n1. Сортировка по полю 'Зарплата от...'")
        print("2. Сортировка по полю 'Зарплата до...'")
        method = input("Поле ввода: ")
        if method == "1":
            Vacancy.set_compare_method(CompareMethodMinSalary())
        elif method == "2":
            Vacancy.set_compare_method(CompareMethodMaxSalary())
        else:
            print("Только 1 или 2")
            continue


def print_table(vacancies: list):
    """Выводит итоговую таблицу с отсортированными и отфильтрованными вакансиями"""

    # Формирование красивой таблицы по максимальным длинам полей
    col_1 = len(max(vacancies, key=lambda x: len(x.city)).city) + 2
    col_4 = len(max(vacancies, key=lambda x: len(x.url)).url) + 2
    col_5 = len(max(vacancies, key=lambda x: len(x.name)).name) + 2

    print(f"\n{'Город'.center(col_1)}"
          f"{'З/П от'.ljust(8)}"
          f"{'З/П до'.ljust(8)}"
          f"{'Ссылка'.center(col_4)}"
          f"{'Наименование'.center(col_5)}"
          f"{'Требования'}"
          )
    print("_" * 200)

    for vacancy in vacancies:
        pay_from = "---"
        pay_to = "---"

        if vacancy.salary[0] > 0:
            pay_from = str(vacancy.salary[0])
        if vacancy.salary[1] > 0:
            pay_to = str(vacancy.salary[1])

        city = vacancy.city.ljust(col_1, ' ')
        pay_from = pay_from.ljust(8, ' ')
        pay_to = pay_to.ljust(8, ' ')
        url = vacancy.url.ljust(col_4, ' ')
        name = vacancy.name.ljust(col_5, ' ')
        requirements = vacancy.requirements
        print(city, pay_from, pay_to, url, name, requirements, sep="")
