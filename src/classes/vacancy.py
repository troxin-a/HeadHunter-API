from abc import ABC, abstractmethod


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


class Vacancy:
    """
    Класс Вакансия, объекты которого можно сравнивать между собой по зарплате
    Для этого необходимо назначить compare_method
    """
    __compare_method: CompareMethod = None  # метод сравнения вакансий (по минимальной/максимальной зарплате)

    __slots__: tuple[str, str, tuple, str] = (
        "name",  # название вакансии
        "city",  # город
        "url",  # ссылка на вакансию
        "_salary",  # зарплата (минимальная, максимальная)
        "requirements"  # требования
    )

    def __init__(self, name: str, city: str, url: str, salary: (dict, None), requirements: str):
        self.name = name
        self.city = city
        self.url = url
        self.salary = salary
        self.requirements = requirements

    def __str__(self):
        pay_from = ""
        pay_to = ""

        if self.salary == (0, 0):
            salary = "не указана"
        else:
            if self.salary[0] != 0:
                pay_from = f"от {self.salary[0]} "
            if self.salary[1] != 0:
                pay_to = f"до {self.salary[1]}"
            salary = (f"{pay_from}{pay_to}").strip()

        return f"{self.name}, {self.city}. Зарплата: {salary}"

    @property
    def salary(self) -> tuple:
        return self._salary

    @salary.setter
    def salary(self, value: (dict, None)):
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
        elif value is None:
            self._salary = (0, 0)
        else:
            raise TypeError(f"Ожидается dict или None, но не {type(value)}")

    @staticmethod
    def validate_before_compare(compare_method, obj1, obj2):
        if not isinstance(obj1, obj2):
            raise TypeError(f"Сравнивать можно только вакансии, но не {type(obj2)}")
        if compare_method is None:
            raise RuntimeError("Необходимо назначить метод сравнения по зарплате")

    @classmethod
    def set_compare_method(cls, value):
        if not issubclass(value.__class__, CompareMethod):
            raise TypeError(f"Указан неверный тип: {type(value)}. Должен быть объект класса CompareMethod")
        cls.__compare_method = value

    def __eq__(self, other):
        self.validate_before_compare(self.__compare_method, other, self.__class__)
        return self.__compare_method.eq(self, other)

    def __lt__(self, other):
        self.validate_before_compare(self.__compare_method, other, self.__class__)
        return self.__compare_method.lt(self, other)

    def __le__(self, other):
        self.validate_before_compare(self.__compare_method, other, self.__class__)
        return self.__compare_method.le(self, other)
