import psycopg2


class DBManager:

    def __init__(self, connect_property):
        self.__connect_property = connect_property

        # Подготовка новой базы данных к работе
        try:
            self.__create_tables()
        except psycopg2.OperationalError:
            self.__create_database()
            self.__create_tables()

    def __create_database(self):
        """
        Метод создает базу данных, если ее нет
        """
        connect_property_without_db = {
            key: value
            for key, value in self.__connect_property.items()
            if key != "dbname"
        }
        conn = psycopg2.connect(**connect_property_without_db)
        cur = conn.cursor()
        conn.autocommit = True
        cur.execute(f"CREATE DATABASE {self.__connect_property['dbname']};")
        cur.close()
        conn.close()
        print(f"База {self.__connect_property['dbname']} создана")

    def __request_db(self, request) -> list:
        """
        Выполняет запрос к базе данных
        """
        with psycopg2.connect(**self.__connect_property) as conn:
            # Открытие курсора
            with conn.cursor() as cur:
                cur.execute(request)
                # Если курсору есть чего вернуть, возвращаем, либо выход
                try:
                    return cur.fetchall()
                except psycopg2.ProgrammingError:
                    return

    def __create_tables(self):
        """
        Метод создает необходимые таблицы, если их нет
        """
        query = """
                CREATE TABLE IF NOT EXISTS companies(
                    company_id int PRIMARY KEY,
                    company_name varchar(100) NOT NULL
                );

                CREATE TABLE IF NOT EXISTS vacancies
                (
                    vacancy_id serial PRIMARY KEY,
                    company_id int REFERENCES companies(company_id) NOT NULL,
                    vacancy_name varchar(100) NOT NULL,
                    city varchar(50) NOT NULL,
                    url varchar(50) NOT NULL,
                    salary_from int,
                    salary_to int,
                    requirements text
                );
                """
        self.__request_db(query)

    def clear_db(self):
        query = """
                TRUNCATE vacancies RESTART IDENTITY;
                TRUNCATE companies CASCADE;
                """
        self.__request_db(query)

    def add_vacancies(self, vacancies: list):
        """
        Принимает список экземпляров класса vacancy,
        Записывает все атрибуты __slots__ с их значениями в 2 таблицы: companies и vacancies
        """

        query = ""
        for vacancy in vacancies:
            query += f"""
                    INSERT INTO companies
                    SELECT
                    '{vacancy.company_id}', '{vacancy.company_name}'
                    WHERE NOT EXISTS (
                        SELECT 1 FROM companies WHERE company_id = '{vacancy.company_id}'
                    );

                    INSERT INTO vacancies (company_id, vacancy_name, city, url, salary_from, salary_to, requirements)
                    VALUES (
                        '{vacancy.company_id}',
                        '{vacancy.vacancy_name}',
                        '{vacancy.city}',
                        '{vacancy.url}',
                        '{vacancy.salary[0]}',
                        '{vacancy.salary[1]}',
                        '{vacancy.requirements}'
                    );
                    """

        self.__request_db(query)

    def delete_vacancy(self, url: str):
        """
        Удаляет запись из таблицы vacancies по url-адресу
        """
        query = f"DELETE FROM vacancies WHERE url = '{url}';"
        self.__request_db(query)

    def get_companies_and_vacancies_count(self) -> list:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        query = """
                SELECT company_name, vacancies.count
                FROM companies
                    JOIN (
                        SELECT company_id, COUNT(vacancy_id) AS count
                        FROM vacancies
                        GROUP BY company_id
                        ) AS vacancies USING(company_id)
                ORDER BY count DESC;
                """
        return self.__request_db(query)

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        query = """
                SELECT company_name, vacancy_name, salary_from, salary_to, url
                FROM vacancies
                JOIN companies USING(company_id);
                """
        return self.__request_db(query)

    def get_avg_salary(self):
        """
        получает среднюю зарплату по вакансиям.
        """
        query = """
                SELECT AVG((salary_from+salary_to)/2)
                FROM vacancies;
                """
        avg_salary = self.__request_db(query)[0][0]
        return avg_salary

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        avg_salary = self.get_avg_salary()
        query = f"""
                SELECT company_name, vacancy_name, salary_from, salary_to, url
                FROM vacancies
                JOIN companies USING(company_id)
                JOIN (
                    SELECT vacancy_id, (salary_from+salary_to)/2 as avg_salary
                    FROM vacancies
                    ) AS salary USING(vacancy_id)
                WHERE avg_salary > {avg_salary}
                ORDER BY avg_salary DESC
                """
        return self.__request_db(query)

    def get_vacancies_with_keyword(self, word):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        query = f"""
                SELECT company_name, vacancy_name, salary_from, salary_to, url
                FROM vacancies
                JOIN companies USING(company_id)
                WHERE LOWER(vacancy_name) LIKE LOWER('%{word}%')
                """
        return self.__request_db(query)
