def get_vacancy_params(vacancy_data):
    """
    Получает данные вакансии из JSON строки
    :param vacancy_data: JSON строка с данными вакансии
    :return: кортеж с данными вакансии
    """

    vacancy_id = int(vacancy_data.get('id'))
    vacancy_name = vacancy_data.get('name')
    salary_from = vacancy_data.get('salary').get('from')
    salary_to = vacancy_data.get('salary').get('to')
    currency = vacancy_data.get('salary').get('currency')
    vacancy_area = vacancy_data.get('area').get('name')
    employer_id = vacancy_data.get('employer').get('id')
    return vacancy_id, vacancy_name, salary_from, salary_to, currency, vacancy_area, employer_id


def get_employer_params(company_data):
    """
    Получает данные работодателя из JSON строки
    :param company_data: JSON строка с данными работодателя
    :return: кортеж с данными работодателя
    """

    employer_id = int(company_data.get('id'))
    employer_name = company_data.get('name')
    employer_url = company_data.get('url')
    return employer_id, employer_name, employer_url


def get_unique_employers(employers, db_employers):
    """
    Получает список работодателей не добавленных в базу данных
    :param employers: работодатели полученные в ходе поиска
    :param db_employers: работодатели добавленные в базу данных
    :return: Список уникальных работотаделей (не добавленных в базу данных)
    """

    db_employers_id = [employer[0] for employer in db_employers]
    unique_employers = [employer for employer in employers if employer[0] not in db_employers_id]
    return unique_employers


def get_unique_vacancies(vacancies, db_vacancies):
    """
    Получает список вакансий не добавленных в базу данных
    :param vacancies: вакансии полученные в ходе поиска
    :param db_vacancies: вакансии добавленные в базу данных
    :return: Список уникальных вакансий (не добавленных в базу данных)
    """

    db_vacancies_id = [vacancy[0] for vacancy in db_vacancies]
    unique_vacancies = [vacancy for vacancy in vacancies if vacancy[0] not in db_vacancies_id]
    return unique_vacancies
