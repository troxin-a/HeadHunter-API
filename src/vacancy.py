from abc import ABC, abstractmethod
from typing import Union


class CompareMethod(ABC):
    """
    Абстрактный класс для методов сравнения
    """

    @staticmethod
    @abstractmethod
    def eq(vac1, vac2):
        pass

    @staticmethod
    @abstractmethod
    def lt(vac1, vac2):
        pass

    @staticmethod
    @abstractmethod
    def le(vac1, vac2):
        pass


class CompareMethodMinSalary(CompareMethod):
    """
    Метод сравнения по Минимальной зарплате
    """

    @staticmethod
    def eq(vac1, vac2):
        return vac1.salary[0] == vac2.salary[0]

    @staticmethod
    def lt(vac1, vac2):
        return vac1.salary[0] < vac2.salary[0]

    @staticmethod
    def le(vac1, vac2):
        return vac1.salary[0] <= vac2.salary[0]


class CompareMethodMaxSalary(CompareMethod):
    """
    Метод сравнения по Максимальной зарплате
    """

    @staticmethod
    def eq(vac1, vac2):
        return vac1.salary[1] == vac2.salary[1]

    @staticmethod
    def lt(vac1, vac2):
        return vac1.salary[1] < vac2.salary[1]

    @staticmethod
    def le(vac1, vac2):
        return vac1.salary[1] <= vac2.salary[1]


class AttrFormater(ABC):
    @staticmethod
    @abstractmethod
    def get_attrs(vacancy: dict):
        pass


class AttrFormaterFromHHRU(AttrFormater):
    @staticmethod
    def get_attrs(vacancy: dict) -> tuple:
        name = vacancy.get("name")
        city = vacancy.get("area").get("name")
        url = vacancy.get("alternate_url")
        salary = vacancy.get("salary")
        requirements = vacancy.get("snippet").get("requirement")

        return name, city, url, salary, requirements


class AttrFormaterFromFile(AttrFormater):
    @staticmethod
    def get_attrs(vacancy: dict) -> tuple:
        name = vacancy.get("name")
        city = vacancy.get("city")
        url = vacancy.get("url")
        salary = vacancy.get("_salary")
        requirements = vacancy.get("requirements")

        return name, city, url, salary, requirements


class Vacancy:
    """
    Класс Вакансия, объекты которого можно сравнивать между собой по зарплате
    Для этого необходимо назначить compare_method
    """

    __compare_method: CompareMethod = (
        None  # метод сравнения вакансий (по минимальной/максимальной зарплате)
    )

    __slots__: tuple[str, str, tuple, str] = (
        "name",  # название вакансии
        "city",  # город
        "url",  # ссылка на вакансию
        "_salary",  # зарплата (минимальная, максимальная)
        "requirements",  # требования
    )

    def __init__(
        self,
        name: str,
        city: str,
        url: str,
        salary: Union[dict, None],
        requirements: str,
    ):
        self.name = name
        self.city = city
        self.url = url
        self.salary = salary
        self.requirements = requirements

    def __str__(self):
        return f"{self.name}. {self.city}, {self._salary}"

    @property
    def salary(self) -> tuple:
        return self._salary

    @salary.setter
    def salary(self, value: Union[dict, None]):
        if isinstance(value, dict):
            if value.setdefault("from", 0):
                salary_from = value["from"]
            else:
                salary_from = 0

            if value.setdefault("to", 0):
                salary_to = value["to"]
            else:
                salary_to = 0
            self._salary = (salary_from, salary_to)
        elif isinstance(value, list):
            self._salary = (value[0], value[1])
        elif value is None:
            self._salary = (0, 0)
        else:
            raise TypeError(f"Ожидается dict или None, но не {type(value)}")

    @classmethod
    def create_vacancies(cls, attr_formater: AttrFormater, data: list) -> list:
        """
        Метод создает список объектов класса Vacancy и возвращает его.
        - Первым аргументом принимает объект класса AttrFormater, выбрав метод формирования атрибутов
        - Далее json (список словарей с вакансиями)
        """

        objects = []
        for vacancy in data:
            attrs = attr_formater.get_attrs(vacancy)
            objects.append(cls(*attrs))
        return objects

    @classmethod
    def validate_before_compare(cls, other):
        if not isinstance(other, cls):
            raise TypeError(f"Сравнивать можно только вакансии, но не {type(other)}")
        if cls.__compare_method is None:
            raise RuntimeError("Необходимо назначить метод сравнения по зарплате")

    @classmethod
    def set_compare_method(cls, value):
        if not issubclass(value.__class__, CompareMethod):
            raise TypeError(
                f"Указан неверный тип: {type(value)}. Должен быть объект класса CompareMethod"
            )
        cls.__compare_method = value

    def __eq__(self, other):
        self.validate_before_compare(other)
        return self.__compare_method.eq(self, other)

    def __lt__(self, other):
        self.validate_before_compare(other)
        return self.__compare_method.lt(self, other)

    def __le__(self, other):
        self.validate_before_compare(other)
        return self.__compare_method.le(self, other)
