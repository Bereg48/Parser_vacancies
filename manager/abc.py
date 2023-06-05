from colorama import init, Fore, Back, Style

init()
import json
import os
from abc import ABC, abstractmethod
import requests

url_hh = 'https://api.hh.ru/vacancies'
url_sj = 'https://api.superjob.ru/2.0/vacancies/?t=4&count=100'

API_KEY_SUPER_JOB = os.environ.get('API_KEY_SUPER_JOB')


class VacanciesGETClass(ABC):
    """ Класс получения вакансий с HeadHunter"""  # класс работы с API (HH, SJ)

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(VacanciesGETClass):

    def __init__(self, search_query):
        """
        Метод инициализации.
        Аргументы:
            text - Текст фильтра
            area - Поиск осуществляется по вакансиям города Москвы
            page - Индекс страницы поиска на HH
            per_page - Кол-во вакансий на 1 странице
            only_with_salary - показатель вакансий только с указанием зарплаты
        """
        # Справочник для параметров GET-запроса
        self.params = {
            'text': search_query,
            'area': 1,
            'page': None,
            'per_page': 100,
            'only_with_salary': True

        }
        self.vacancies = []

    def get_request(self):
        """
        Метод для получения страницы со списком вакансий.
        """

        response = requests.get(url_hh, params=self.params)  # Посылаем запрос к API
        return response.json()["items"]

    def modify_data(self):
        """
        Метод для реализации требуемого формата вывода вакансий.
        """
        form_vacancies = []
        for vacanc in self.vacancies:
            formalized_dict = {
                'name_vacancies': vacanc['name'],
                'organization': vacanc['employer']['name'],
                'salary_from': vacanc['salary']['from'] if vacanc['salary']['from'] is None else 0,
                'salary_to': vacanc['salary']['to'] if vacanc['salary']['to'] is None else 0,
                'experience': vacanc['experience']['name'],
                'requirement': vacanc['snippet']['requirement'],
                'responsibility': vacanc['snippet']['responsibility'],
                'api': 'HeadHunter'
            }
            if type(vacanc['salary']['from']) != int:
                vacanc['salary']['from'] = 0
            else:
                vacanc['salary']['from'] = vacanc['salary']['from']

            if type(vacanc['salary']['to']) != int:
                vacanc['salary']['to'] = 0
            else:
                vacanc['salary']['to'] = vacanc['salary']['to']

            salary = vacanc['salary']
            if salary:
                formalized_dict['salary_from'] = salary['from']
                formalized_dict['salary_to'] = salary['to']
            else:
                formalized_dict['salary_from'] = 0
                formalized_dict['salary_to'] = 0
            form_vacancies.append(formalized_dict)
        return form_vacancies

    def get_vacancies(self, pages_count=2):
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params['page'] = page
            print(Fore.GREEN + f"({self.__class__.__name__}) страница № {page + 1} -", end=" ")
            page_vacancies = self.get_request()
            self.vacancies.extend(page_vacancies)
            print(Fore.GREEN + f"Загружено вакансий: {len(page_vacancies)}")
            if len(page_vacancies) == 0:
                break


class SuperJobAPI(VacanciesGETClass):

    def __init__(self, search_query):
        """
        Метод инициализации.
        Аргументы:
            keyword - Текст фильтра
            town - Поиск осуществляется по вакансиям города Москвы
            count - Кол-во вакансий на 1 странице
        """
        # Справочник для параметров GET-запроса
        self.params = {'town': 4,
                       'count': 100,
                       'keyword': search_query

                       }
        self.vacancies = []

    def get_request(self):
        """
        Метод для получения страницы со списком вакансий.
        """
        headers = {'X-Api-App-Id': API_KEY_SUPER_JOB}
        response = requests.get(url_sj, params=self.params, headers=headers)  # Посылаем запрос к API
        return response.json()["objects"]

    def modify_data(self):
        """
        Метод для реализации требуемого формата вывода вакансий.
        """
        form_vacancies = []
        for vacanc in self.vacancies:
            formalized_dict = {
                'name_vacancies': vacanc['profession'],
                'organization': vacanc['firm_name'],
                'salary_from': vacanc['payment_from'],
                'salary_to': vacanc['payment_to'],
                'experience': vacanc['experience']['title'],
                'requirement': vacanc['vacancyRichText'],
                'responsibility': vacanc['candidat'],
                'api': 'SuperJob'
            }
            form_vacancies.append(formalized_dict)
        return form_vacancies

    def get_vacancies(self, pages_count=2):
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params['page'] = page
            print(Fore.BLUE + f"({self.__class__.__name__}) страница № {page + 1} -", end=" ")
            page_vacancies = self.get_request()
            self.vacancies.extend(page_vacancies)
            print(Fore.BLUE + f"Загружено вакансий: {len(page_vacancies)}")
            if len(page_vacancies) == 0:
                break
