import psycopg2


class DBManager:
    """
    Класс для работы с базлй данных
    """

    def __init__(self, db_host, db_name, db_user, db_password):
        """
        Инициализатор класса
        :param db_host:Хост базы данных
        :param db_name: Имя базы данных
        :param db_user: Имя пользователя базы данных
        :param db_password: Пароль пользователя базы данных
        """

        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def get_connection(self) -> psycopg2.connect:
        """
        Устанавливает соединение с базой данных
        :return: Объект соединени с базой данных
        """

        connection = psycopg2.connect(
            host=self.db_host,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password
        )
        return connection

    def execute_query(self, query, data=None):
        """
        Выполняет SQL запрос. При получении данных выполняет executemany
        :param query: SQL запрос
        :param data: данные для добавления в базу данных
        :return: None
        """

        connection = self.get_connection()
        cursor = connection.cursor()
        if data:
            cursor.executemany(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

    def create_database(self):
        """
        Создает базу данных если она еще не создана
        :return: None
        """

        try:
            connection = psycopg2.connect(host=self.db_host, user=self.db_user, password=self.db_password)
            connection.autocommit = True
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE {self.db_name}")
        except psycopg2.Error:
            print("База данных уже создана")

    def create_tables(self):
        """
        Создает таблицы если они еще не созданы
        :return: None
        """

        create_table_query = """
                CREATE TABLE IF NOT EXISTS employers(
                    employer_id SERIAL PRIMARY KEY,
                    employer_name VARCHAR(255),
                    employer_url VARCHAR(255)
                );

                CREATE TABLE IF NOT EXISTS vacancies(
                    vacancy_id SERIAL PRIMARY KEY,
                    vacancy_name VARCHAR(255),
                    salary_from INT,
                    salary_to INT,
                    currency VARCHAR(10),
                    vacancy_area VARCHAR(255),
                    employer_id INT REFERENCES employers(employer_id)
                );"""
        self.execute_query(create_table_query)

    def insert_new_vacancies(self, vacancies):
        """
        Добавляет полученные вакансии в базу данных
        :param vacancies: Список кортежей с даннымми полученныз вакансий
        :return: None
        """

        if vacancies:
            symbols = ", ".join(["%s"] * len(vacancies[0]))
            keys = "vacancy_id, vacancy_name, salary_from, salary_to, currency, vacancy_area, employer_id"
            insert_vacancies_query = f"INSERT INTO vacancies ({keys}) VALUES ({symbols})"
            self.execute_query(insert_vacancies_query, vacancies)

    def insert_new_employers(self, employers):
        """
        Добавляет полученных работодателей в базу данных
        :param employers: Список кортежей с данными работодателя
        :return: None
        """

        if employers:
            symbols = ", ".join(["%s"] * len(employers[0]))
            keys = "employer_id, employer_name, employer_url"
            insert_vacancies_query = f"INSERT INTO employers ({keys}) VALUES ({symbols})"
            self.execute_query(insert_vacancies_query, employers)

    def get_vacancies_by_employer(self, employer_id):
        """
        Получает список вакансии по ID работодателя
        :param employer_id: ID работодателя
        :return: Список кортежей с вакансиями определенного работодателя
        """

        with self.get_connection() as connection, connection.cursor() as cursor:
            search_query = f"SELECT * FROM vacancies WHERE vacancies.employer_id={employer_id}"
            cursor.execute(search_query)
            search_result = cursor.fetchall()
            return search_result

    def get_all_employers(self):
        """
        Получает список всех работодателей, имеющихся в базе данных.
        :return: Список кортежей со всеми работодателями.
        """

        with self.get_connection() as connection, connection.cursor() as cursor:
            query = "SELECT * FROM employers"
            cursor.execute(query)
            all_employers = cursor.fetchall()
            return all_employers

    def get_all_vacancies(self):
        """
        Получает список всех вакансий, имеющихся в базе данных.
        :return: Список кортежей со всеми вакансиями.
        """

        with self.get_connection() as connection, connection.cursor() as cursor:
            query = "SELECT * FROM vacancies"
            cursor.execute(query)
            all_vacancies = cursor.fetchall()
            return all_vacancies

    def get_employers_and_vacancies_count(self):
        """
        Получет список компаний отсортированный по убыванию количества вакансий
        :return: Список кортежей с названиями компаний и количеством открытых ваккансий у них
        """

        with self.get_connection() as connection, connection.cursor() as cursor:
            query = """SELECT e.employer_name, COUNT(v.vacancy_id) as vacancy_count
                        FROM employers e
                        LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                        GROUP BY e.employer_name
                        ORDER BY vacancy_count DESC;"""
            cursor.execute(query)
            count_vacancies = cursor.fetchall()
            return count_vacancies

    def get_vacancies_with_higher_salary(self):
        """
        Получает список вакансий с зарплатой выше средней
        :return: Список кортежей с вакансиями у которых зарплата выше средней.
        """

        with self.get_connection() as connection, connection.cursor() as cursor:
            query = """SELECT *
                        FROM vacancies v
                        JOIN employers e ON v.employer_id = e.employer_id
                        WHERE v.salary_from > (
                        SELECT AVG(salary_from) FROM vacancies
                        );"""
            cursor.execute(query)
            vacancies_with_higher_salary = cursor.fetchall()
            return vacancies_with_higher_salary

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по всем вакансиям
        :return: Средняя зарплата типа int по всем вакансиям округленная до целого числа
        """

        with self.get_connection() as connection, connection.cursor() as cursor:
            query = "SELECT AVG(salary_from) FROM vacancies;"
            cursor.execute(query)
            avg_salary = cursor.fetchone()[0]
            return int(avg_salary)

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список вакансий в которых присутсвует ключевое слово
        :param keyword: Ключевое слово для поиска
        :return: Список кортежей с вакансиями по ключевому слову
        """

        with self.get_connection() as connection, connection.cursor() as cursor:
            query = f"SELECT * FROM vacancies WHERE LOWER(vacancy_name) LIKE LOWER('%{keyword}%')"
            cursor.execute(query)
            vacancies_with_keyword = cursor.fetchall()
            return vacancies_with_keyword
