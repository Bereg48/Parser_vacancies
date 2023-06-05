class Vacancy:
    """Класс инициализирующий элементы, а также задает строковое представление"""

    def __init__(self, vacanc):
        self.name_vacancies = vacanc['name_vacancies']
        self.organization = vacanc['organization']
        self.salary_from = vacanc['salary_from'] if vacanc['salary_from'] is None else 0
        self.salary_to = vacanc['salary_to'] if vacanc['salary_to'] is None else 0
        self.experience = vacanc['experience']
        self.requirement = vacanc['requirement']
        self.responsibility = vacanc['responsibility']
        self.api = vacanc['api']

    def __str__(self):
        if not self.salary_from and not self.salary_to:
            salary = "Не указана"
        else:
            salary_from, salary_to = "", ""
            if self.salary_from:
                salary_from = f"от {self.salary_from}"
            if self.salary_to:
                salary_to = f"до {self.salary_to}"
            salary = " ".join([salary_from, salary_to]).strip()
        return f"""
Вакансия: \"{self.name_vacancies}\"
Компания: \"{self.organization}\"
Зарплата: \"{salary}\"
Опыт работы: \"{self.experience}\"
Требования: \"{self.requirement}\"
Обязанности: \"{self.responsibility}\"
Портал размещения: \"{self.api}\" 
------------------------------------------------------------------------------------------------------------------------
"""
