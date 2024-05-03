import json
from abc import ABC, abstractmethod

import requests


class AbstractConnect(ABC):
    @abstractmethod
    def connect(self):
        pass


class Connect(AbstractConnect):
    """
    Класс для работы с платформой hh.ru. Подключается к API и получает вакансии в формате json
    """
    address: str

    def __init__(self, address: str):
        self.address = address

    def connect(self) -> dict:
        response = requests.get(self.address)
        if response.status_code == 200:
            vacancies = json.loads(response.content)["items"]
            return vacancies
        else:
            return {}
