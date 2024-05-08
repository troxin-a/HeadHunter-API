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

    @staticmethod
    def connect(url: str) -> list:
        response = requests.get(url)
        if response.status_code == 200:
            vacancies = json.loads(response.content)["items"]
            return vacancies
        else:
            return []
