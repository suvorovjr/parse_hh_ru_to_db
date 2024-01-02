import os
from src.hh_api import HhApi
from src.DBManager import DBManager
from src.vacancy_ui import UserInterface
from src.vacancy import Vacancy
from src.employer import Employer
from src.utils import get_vacancy_params, get_employer_params, get_unique_employers, get_unique_vacancies

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def main():
    # Список интересующих компаний
    target_companies = ['Тинькофф', 'Компания Лимарк', 'Carbon Soft', 'Тензор', 'ЭР-Телеком',
                        'KVINT', 'InfiNet Wireless', 'URALNIX', 'OmniLine', 'УрГУПС']

    # Создание экземпляра класса для работы с БД
    db_manager = DBManager(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)

    # Создание БД если она еще не создана
    db_manager.create_database()

    # Создание таблиц в БД если они еще не созданы
    db_manager.create_tables()

    while True:
        user_input = UserInterface.main_menu()
        if user_input == "1":
            keyword = input("Введите ключевое слово для поиска\n")
            api_client = HhApi(target_companies, keyword)
            api_client.search_companies_by_name()
            api_client.search_vacancies_by_company_id()
            employers = [get_employer_params(company) for company in api_client.get_companies_descriptions()]
            vacancies = [get_vacancy_params(vacancy) for vacancy in api_client.get_vacancies()]
            db_employers = db_manager.get_all_employers()
            db_vacancies = db_manager.get_all_vacancies()
            unique_employers = get_unique_employers(employers, db_employers)
            unique_vacancies = get_unique_vacancies(vacancies, db_vacancies)
            db_manager.insert_new_employers(unique_employers)
            db_manager.insert_new_vacancies(unique_vacancies)
        elif user_input == "2":
            new_target_company = input("Введите название компании для добавления в список\n")
            lower_companies = [company.lower() for company in target_companies]
            if new_target_company.lower() not in lower_companies:
                target_companies.append(new_target_company)
                print("Компания успешно добавлена")
            else:
                print("Компания уже есть в списке")
        elif user_input == "3":
            search_company = input("Введите название компании для поиска в базе данных\n")
            db_employers = db_manager.get_all_employers()
            search_id = [employer[0] for employer in db_employers if employer[1].lower() == search_company.lower()]
            if search_id:
                db_vacancies = db_manager.get_vacancies_by_employer(search_id[0])
                if db_vacancies:
                    [print(Vacancy(vacancy)) for vacancy in db_vacancies]
                else:
                    print('У этой компании нет вакансий по заданным запросам')
            else:
                print("Такой компании нет в списке")
        elif user_input == "4":
            db_employers = db_manager.get_employers_and_vacancies_count()
            [print(Employer(employer)) for employer in db_employers]
        elif user_input == "5":
            db_vacancies = db_manager.get_all_vacancies()
            [print(Vacancy(vacancy)) for vacancy in db_vacancies]
        elif user_input == "6":
            avg_salary = db_manager.get_avg_salary()
            print(f'Средняя зарплата = {avg_salary}')
        elif user_input == "7":
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            [print(Vacancy(vacancy)) for vacancy in vacancies_with_higher_salary]
        elif user_input == "8":
            keyword_for_search = input('Введите ключевое слово для поиска вакансий\n')
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword_for_search)
            [print(Vacancy(vacancy)) for vacancy in vacancies_with_keyword]
        elif user_input == "9":
            break


if __name__ == "__main__":
    main()
