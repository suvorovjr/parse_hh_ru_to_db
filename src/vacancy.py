class Vacancy:
    """
    Класс для работы с вакансиями
    """

    def __init__(self, data):
        """
        Инициализатор класса
        :param data: информация о вакансии в виде tuple
        """

        self.vacancy_id = data[0]
        self.vacancy_name = data[1]
        self.salary_from = data[2]
        self.salary_to = data[3]
        self.currency = data[4]
        self.vacancy_area = data[5]
        self.employer_id = data[6]

    def __str__(self):
        return f"Вакансия: {self.vacancy_name}. Зарплата от {self.salary_from} до {self.salary_to} {self.currency}. " \
               f"Компания: {self.employer_id}. "

    def __repr__(self):
        return f"Vacancy(vacancy_id={self.vacancy_id}, vacancy_name={self.vacancy_name}, salary_from={self.salary_from}," \
               f" salary_to={self.salary_to}, currency={self.currency}, vacancy_area={self.vacancy_area}, " \
               f"employer_id={self.employer_id}"
