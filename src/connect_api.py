import json
from abc import ABC, abstractmethod

import requests


class AbstractConnectAPI(ABC):
    @staticmethod
    @abstractmethod
    def connect(url):
        pass


class ConnectAPI(AbstractConnectAPI):
    """
    Класс для работы с платформой hh.ru. Подключается к API и получает вакансии в формате json
    """

    def __init__(self):
        self.base_query = {
            'text': "",
            'page': 0,
            'per_page': 0,
            'area': 113,
        }
        self.url = "https://api.hh.ru/vacancies"

    def connect(self, query: dict) -> list:
        response = requests.get(self.url, query)
        if response.status_code == 200:
            vacancies = json.loads(response.content)["items"]
            return vacancies
        else:
            return []

    def get_vacancies_data(self, text: str, quantity: int):
        """
        Метод загружает вакансии по ключевому слову.
        Принимает название вакансии и количество.
        Возвращает вакансии в виде json-списка.
        """

        # В базовый словарь параметров запроса пишем поисковую вакансию
        self.base_query["text"] = text

        if quantity > 2000:
            quantity = 2000
        quantity = abs(quantity)

        # Определяем, по сколько вакансий нужно запрашивать в каждой итерации запроса
        pages = [100 for _ in range(quantity // 100)]
        pages.append(quantity % 100)
        per_page = iter(pages)

        print("\nЗагрузка...")
        data = []
        for page in range(len(pages)):
            self.base_query["page"] = page
            self.base_query["per_page"] = next(per_page)

            items = self.connect(self.base_query)
            data.extend(items)

            # Считаем прогресс и выводим на экран
            download_progress = round(100 / (len(pages) / (page + 1)))
            print(f"Загружено {download_progress}%")
        print("Загрузка завершена\n")

        return data
