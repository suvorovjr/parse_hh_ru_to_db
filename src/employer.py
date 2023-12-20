class Employer:
    """
    Класс для работы с работодателями
    """

    def __init__(self, data):
        """
        Инициализатор класса
        :param data: информация о вакансии в виде tuple
        """

        self.employer_name = data[0]
        self.vacancies_count = data[1]

    def __str__(self):
        return f"У компании: {self.employer_name} {self.vacancies_count} открытых вакансий по вашим запросам."

    def __repr__(self):
        return f"Employer(employer_name={self.employer_name}, vacancies_count={self.vacancies_count}"
