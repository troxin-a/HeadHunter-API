import sys
from abc import ABC, abstractmethod

import requests


class AbstractConnectAPI(ABC):
    @abstractmethod
    def _connect(self, url: str, query: dict = None):
        pass

    def _get_info_about_employer(self, employer_id: int):
        pass

    def get_vacancies_data(self, employer_id: int):
        pass


class ConnectAPI(AbstractConnectAPI):
    """
    Класс для работы с платформой hh.ru. Подключается к API и получает вакансии в формате json
    """

    def __init__(self):
        self.__base_query = {
            "employer_id": 0,
            "page": 0,
            "per_page": 0,
            "area": 113,
        }
        self.__url = "https://api.hh.ru/vacancies"

    def _connect(self, url: str, query: dict = None) -> list:
        if query is None:
            query = {}
        response = requests.get(url, query, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data
        return []

    def _get_info_about_employer(self, employer_id: int):
        """
        Получает наименование компании и количество вакансий по его id
        """
        url = f"https://api.hh.ru/employers/{employer_id}"
        data = self._connect(url)

        # Если не находит вакансию, выходим
        try:
            name = data["name"]
            quantity = data["open_vacancies"]
        except Exception:
            return None, None

        return name, quantity

    def get_vacancies_data(self, employer_id: int):
        """
        Метод загружает вакансии по id работодателя.
        Принимает название вакансии.
        Возвращает вакансии в виде словарей.
        """

        # В базовый словарь параметров запроса пишем поисковую компанию
        self.__base_query["employer_id"] = employer_id

        name, quantity = self._get_info_about_employer(employer_id)
        if not name:
            return

        # Определяем, по сколько вакансий нужно запрашивать в каждой итерации запроса
        pages = [100 for _ in range(quantity // 100)]
        pages.append(quantity % 100)

        print("")
        print(f"Компания {name}. Активных вакансий: {quantity}")
        bar_length = 50

        sys.stdout.write("\r")
        sys.stdout.write("Загрузка: [{:{}}] {:>3}%".format("", bar_length, 0))
        data = []
        for page, per_page in enumerate(pages):
            self.__base_query["page"] = page
            self.__base_query["per_page"] = per_page

            items = self._connect(self.__url, self.__base_query)["items"]
            data.extend(items)

            # Считаем прогресс и выводим на экран
            percent = round(100 / (len(pages) / (page + 1)))
            sys.stdout.write("\r")
            sys.stdout.write(
                "Загрузка: [{:{}}] {:>3}%".format(
                    "=" * int(percent / (100.0 / 50)), bar_length, int(percent)
                )
            )
            sys.stdout.flush()

        print("\n")

        return data
