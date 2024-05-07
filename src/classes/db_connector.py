from abc import ABC, abstractmethod
from os import path, remove
import json


class AbstractDBConnector(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, selections: tuple):
        pass


class DBConnector(AbstractDBConnector):
    """
    Класс добавляет в json вакансии
    получает данные из файла по указанным критериям,
    удаляет вакансии по URL
    """

    def __init__(self, file_json: str):
        self.file_json = path.join("data", file_json)

    def read(self) -> list:
        """Читает json и возвращает данные"""
        try:
            with open(self.file_json, "r", encoding="UTF-8") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    return []  # Если файл пустой, возвращаем пустой список
        except FileNotFoundError:
            with open(self.file_json, "w", encoding="UTF-8") as file:
                file.write("[]")
            return []  # Если файл отсутствует, создаем его и возвращаем пустой список
        else:
            return data

    def save(self, data: list):
        """Записывает данные в файл json"""
        json_data = json.dumps(data, ensure_ascii=False)
        with open(self.file_json, "w", encoding="UTF-8") as file:
            file.write(json_data)

    def add_vacancy(self, vacancy):
        """
        Принимает экземпляр класса vacancy,
        дописывает все атрибуты __slots__ с их значениями в json-файл
        """

        data = self.read()
        item = {attr: vacancy.__getattribute__(attr) for attr in vacancy.__slots__}
        data.append(item)
        self.save(data)

    def delete_vacancy(self, vacancy):
        """
        Принимает экземпляр класса vacancy,
        удаляет первую попавшуюся запись, которая соответствует вакансии по ключу URL
        """

        data = self.read()
        item = None
        for vac in data:
            if vac["url"] == vacancy.url:
                item = vac
                break
        if item:
            data.remove(item)
        self.save(data)

    def get_vacancies(self, selections: dict) -> list:
        """
        Принимает словарь, по ключам которого нужно получить вакансии из файла.
        Возвращает данные в виде списка словарей
        """

        data = self.read()

        for key, value in selections.items():
            data = list(filter(lambda x: x[key] == value, data))
        return data
