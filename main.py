from src.db_connector import DBConnector
from src.user_interface import change_start, filter_vacancies

db_connector = DBConnector("vacancies.json")


def user_interaction():
    print("Добро пожаловать в поиск вакансий на hh.ru")

    change_start(db_connector)

    to_exit = ""
    while to_exit == "":
        print("\nНажмите Enter для продолжения.")
        to_exit = input("Для выхода введите любой символ: ")
        if to_exit == "":
            filter_vacancies(db_connector)


if __name__ == "__main__":
    user_interaction()
