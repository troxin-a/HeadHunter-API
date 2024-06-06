from src.connect_api import ConnectAPI
from src.dbmanager import DBManager
from src.vacancy import (
    Vacancy,
    CompareMethodMinSalary,
    CompareMethodMaxSalary,
    AttrFormaterFromHHRU,
)


def new_base(db_manager: DBManager, list_employers: list):
    """
    Функция запускает метод загрузки вакансий (по наименованию) в файл
    """

    db_manager.clear_db()

    api = ConnectAPI()
    for employer_id in list_employers:
        vacancies_data = api.get_vacancies_data(employer_id)
        if vacancies_data:
            vacancies = Vacancy.create_vacancies(AttrFormaterFromHHRU(), vacancies_data)
            db_manager.add_vacancies(vacancies)
        else:
            continue


def change_start(db_manager: DBManager, list_employers):
    """
    Функция с диалогом: начать работу с имеющейся базой или загрузить все заново
    """

    method = None
    while method not in ["1", "2"]:
        print("\n1. Загрузить вакансии с hh.ru")
        print("2. Воспользоваться имеющейся базой")
        method = input("Поле ввода: ")
        if method not in ["1", "2"]:
            print("Только 1 или 2")
            continue
        if method == "1":
            new_base(db_manager, list_employers)
        change_method_DBManager(db_manager)


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
    """Выводит итоговую таблицу"""

    # Формирование красивой таблицы по максимальным длинам полей
    if vacancies:
        col_0 = len(max(vacancies, key=lambda x: len(x[0]))[0]) + 2
        col_1 = len(max(vacancies, key=lambda x: len(x[1]))[1]) + 2
        col_4 = len(max(vacancies, key=lambda x: len(x[4]))[4]) + 2
    else:
        col_0, col_1, col_4 = 10, 25, 50

    print(
        f"\n{'Компния'.center(col_0)}"
        f"{'З/П от'.ljust(8)}"
        f"{'З/П до'.ljust(8)}"
        f"{'Вакансия'.center(col_1)}"
        f"{'Ссылка'.center(col_4)}"
    )
    print("_" * 160)

    for vacancy in vacancies:
        pay_from = "---"
        pay_to = "---"

        if vacancy[2] > 0:
            pay_from = str(vacancy[2])
        if vacancy[3] > 0:
            pay_to = str(vacancy[3])

        company = vacancy[0].ljust(col_0, " ")
        name = vacancy[1].ljust(col_1, " ")
        pay_from = pay_from.ljust(8, " ")
        pay_to = pay_to.ljust(8, " ")
        url = vacancy[4].ljust(col_4, " ")

        print(company, pay_from, pay_to, name, url, sep="")


def get_key_word(db_manager: DBManager):
    print()
    word = input("Введите ключевое слово для фильтрации вакансий: ")
    vacancies = db_manager.get_vacancies_with_keyword(word)
    print_table(vacancies)


def change_method_DBManager(db_manager: DBManager):
    change = "9"
    while change not in "12345":
        print(
            "\n"
            + "1. Получить список всех компаний и количество вакансий у каждой компании\n"
            + "2. Получить список всех вакансий\n"
            + "3. Получить среднюю зарплату по вакансиям\n"
            + "4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
            + "5. Получить список всех вакансий по ключевым словам\n"
        )
        change = input("Поле ввода: ")
        if change not in "12345":
            print("Только от 1 до 5")
            continue

    print()
    match change:
        case "1":
            companies = db_manager.get_companies_and_vacancies_count()
            for company in companies:
                print(f"{company[0].ljust(20)}{company[1]} вакансий")
        case "2":
            vacancies = db_manager.get_all_vacancies()
            print_table(vacancies)
        case "3":
            print(round(db_manager.get_avg_salary()))
        case "4":
            vacancies = db_manager.get_vacancies_with_higher_salary()
            print_table(vacancies)
        case "5":
            get_key_word(db_manager)
