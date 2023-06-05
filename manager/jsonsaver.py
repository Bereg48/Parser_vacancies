import json

from manager.vacancy import Vacancy


class JSONSaver:
    """Класс производящий операции с полученным файлом"""

    def __init__(self, search_query, vacancies_json):
        self.filename = f"{search_query.title()}.json"
        self.insert(vacancies_json)

    def insert(self, vacancies_json):
        """Метод insert сохраняет список вакансий в файл соответствующий наименованию запроса"""
        with open(self.filename, mode='w', encoding='utf8') as f:
            json.dump(vacancies_json, f, ensure_ascii=False, indent=4, separators=(",", ":"))

    def select(self):
        """Метод select загружает список вакансий с json далее формирует список вакансий экземпляра класса Vacancy"""
        with open(self.filename, mode='r', encoding='utf8') as f:
            vacancies = json.load(f)
        return [Vacancy(x) for x in vacancies]

    def select_to(self):
        """Метод select_to загружает список вакансий с json далее формирует список вакансий экземпляра класса Vacancy
        с сортировкой вакансии, которые соответствуют запросу, без опыта работы"""
        with open(self.filename, mode='r', encoding='utf8') as f:
            vacancies = json.load(f)
            filter_dict_experience = [user for user in vacancies if user['experience'] in ["Нет опыта", "Не имеет "
                                                                                                        "значения"]]
        return [Vacancy(x) for x in filter_dict_experience]

    def select_tow(self):
        """Метод select_to загружает список вакансий с json далее формирует список вакансий экземпляра класса Vacancy
        с сортировкой вакансии, которые соответствуют запросу, без опыта работы"""
        with open(self.filename, mode='r', encoding='utf8') as f:
            vacancies = json.load(f)
            filter_dict_organization = [user for user in vacancies if user['organization'] in ["Яндекс", "СБЕР",
                                                                                               "SberTech",
                                                                                               "Русатом Сервис",
                                                                                               "Глонасс",
                                                                                               "Российские "
                                                                                               "космические системы",
                                                                                               "СИНЕРГИЯ", "Сбербанк"]]
        return [Vacancy(x) for x in filter_dict_organization]

    def sort_by_salary_from(self):
        """Метод sort_by_salary_from сортирует список вакансий по минимальной зарплате от максимального значения до
        минимального значения минимальной зарплаты DESC и от минимального значения до максимального значения
        минимальной зарплаты ASC"""
        desc = True if input(
            "> - DESC \n"
            "< - ASC \n>>>"
        ).lower() == ">" else False
        vacancies = self.select()
        return sorted(vacancies,
                      key=lambda x: (x.salary_from if x.salary_from else 0, x.salary_to if x.salary_to else 0),
                      reverse=desc)

    def sort_by_salary_to(self):
        """Метод sort_by_salary_to сортирует список вакансий по максимальной зарплате от максимального значения до
        минимального значения максимальной зарплаты DESC и от минимального значения до максимального значения
        максимальной зарплаты ASC"""
        desc = True if input(
            "> - DESC \n"
            "< - ASC \n>>>"
        ).lower() == ">" else False
        vacancies = self.select()
        return sorted(vacancies,
                      key=lambda x: (x.salary_to if x.salary_to else 0, x.salary_from if x.salary_from else 0),
                      reverse=desc)
