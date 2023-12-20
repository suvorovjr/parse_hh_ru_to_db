import requests


class HhApi:
    """
    Класс для работы с сервисом hh.ru по открытому API
    """

    def __init__(self, target_companys, keyword):
        """
        Инициализатор класса
        :param target_companys: Список названий интересующих нас компаний
        :param keyword: Ключевое слово для поиска вакансий
        """
        self.target_companys = target_companys
        self.keyword = keyword
        self.vacancy = []
        self.company_descriptions = []

    def search_companies_by_name(self):
        """
        Получает ID и информацию об всех компаниях по названию, которые заданы в списке
        :return: None
        """

        for company_name in self.target_companys:
            response = requests.get(f"https://api.hh.ru/employers?text={company_name}").json()
            if response["items"]:
                company_description = [comp for comp in response["items"] if comp["name"] == company_name]
                if company_description:
                    self.company_descriptions.append(company_description[0])

    def search_vacancies_by_company_id(self):
        """
        Получает список вакансий по ключевому запросу на основе списка ID полученного в функции get_companys_by_name
        :return: None
        """

        params = {
            "page": 0,
            "per_page": 100,
            "text": self.keyword,
            "only_with_salary": True,
        }
        for company in self.company_descriptions:
            response = requests.get(f'https://api.hh.ru/vacancies?employer_id={company["id"]}', params=params).json()
            if response["items"]:
                all_vacancy = [vacancy for vacancy in response["items"]]
                self.vacancy.extend(all_vacancy)

    def get_vacancies(self):
        """
        Возвращает список вакансий
        :return: список словарей с данными вакансий
        """

        return self.vacancy

    def get_companies_descriptions(self):
        """
        Возвращает список с описанием компаний
        :return: Список словарей с описанием компаний
        """

        return self.company_descriptions
