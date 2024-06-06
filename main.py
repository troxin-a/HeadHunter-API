from src.dbmanager import DBManager
from src.user_interface import change_start, change_method_DBManager
from src.settings import get_settings


settings = get_settings()[0]
list_employers = get_settings()[1]
db_manager = DBManager(settings)


def user_interaction():
    print("Добро пожаловать в поиск вакансий на hh.ru")

    change_start(db_manager, list_employers)

    to_exit = ""
    while to_exit == "":
        print("\nНажмите Enter для продолжения.")
        to_exit = input("Для выхода введите любой символ: ")
        if to_exit == "":
            change_method_DBManager(db_manager)


if __name__ == "__main__":
    user_interaction()
