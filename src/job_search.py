import time
from abc import ABC, abstractmethod
from http import HTTPStatus

import requests
import json


class VacanciesAPI(ABC):
    """Абстрактный класс для платформ HeadHunter, SuperJob для получение API"""

    @abstractmethod
    def get_vacancies(self, text: str):
        pass

    @abstractmethod
    def get_formatted_vacancies(self):
        pass


class HeadHunterAPI(VacanciesAPI):
    """Класс для получения API с платформы HeadHunter"""

    def __init__(self):
        self.items_hh = []

    def get_vacancies(self, text: str):
        """Получение заданных пользователем профессий с платформы HeadHunter"""
        self.items_hh = []
        for page in range(10):
            time.sleep(1)
            api_hh = 'https://api.hh.ru/vacancies'
            params = {
                'per_page': 100,
                "page": page,
                'text': text
            }
            response = requests.get(api_hh, params=params)
            self.items_hh = response.json()['items']
            return self.items_hh

    def get_formatted_vacancies(self):
        """Сортировка вакансий"""
        vacancies = []
        for vacancy in self.get_vacancies('Python'):
            vacancies.append({
                'name': vacancy.get('name'),
                'url:': vacancy.get('alternate_url'),
                'salary': vacancy.get('salary'),
                'requirements': vacancy.get('experience')['name']
            })

        return vacancies


class SuperJobAPI(VacanciesAPI, ABC):
    """"Класс для получения API с платформы SuperJob"""

    def __init__(self):
        self.items_sj = []

    def get_vacancies(self, keyword: str):
        """Получение заданных пользователем профессий с платформы SuperJob"""
        for page in range(10):
            time.sleep(1)
            api_sj = "https://api.superjob.ru/2.0/vacancies/"
            headers = {
                "X-Api-App-Id": 'v3.r.137643549.5dafea9523d8382ad2dd0791d3bb597bb32e4eff'
                                '.6b545afc3b70eeeb7093cd923f7dc0f8b147f2cb'
            }
            params = {
                "keyword": "Python",
                "page": page
            }
            response = requests.get(api_sj,
                                    params=params,
                                    headers=headers)
            if not response.status_code == HTTPStatus.OK:
                return f'Ошибка! Статус: {response.status_code}!'
            self.items_sj = response.json()['objects']
            return self.items_sj

    def get_formatted_vacancies(self):
        """Сортировка вакансий"""
        vacancies = []
        for vacancy in self.get_vacancies('Python'):
            vacancies.append({
                'name': vacancy.get('profession'),
                'url': vacancy.get('link'),
                'salary': f'от {vacancy.get("payment_from")} до {vacancy.get("payment_to")}',
                'requirements': vacancy.get('experience')['title']
            }
            )
        return vacancies


class Vacancies:
    """Класс для работы с вакансиями"""

    def __init__(self, name, url, salary, skills):
        """Инициализация вакансий по заданным атрибутам"""
        self.__name = name
        self.__url = url
        self.__salary = salary
        self.__skills = skills

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, other):
        if isinstance(other.name, str):
            self.name = other.name

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, other):
        if isinstance(other.url, str):
            self.url = other.url

    @property
    def skills(self):
        return self.__skills

    @skills.setter
    def skill(self, other):
        if isinstance(other.skills, str):
            self.skills = other.skills

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, other_salary: str) -> None:
        if isinstance(other_salary, str):
            self.salary = other_salary

    def __str__(self):
        return f"{self.name}, " \
               f"{self.salary}" \
               f"{self.skills}" \
               f"{self.url}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.salary}, {self.skills}, {self.url})"

    def __lt__(self, other):
        return self.salary < other.salary

    def __gt__(self, other):
        return self.salary > other.salary

    @staticmethod
    def validate_attributes(name: str, url: str, salary: str, skills: str) -> None:
        """Статический метод для валидации атрибутов класса"""

        if not isinstance(name, str):
            raise TypeError('Название вакансии должно передаваться быть строкой.')
        if not isinstance(url, str):
            raise TypeError('Передаваемая ссылка должна быть строкой.')
        if not isinstance(salary, str):
            raise TypeError('Зарплата должна передаваться строкой в формате "xxx-yyy"')
        if not isinstance(skills, str):
            raise TypeError('Требования должны передаваться строкой.')


class Json(ABC):
    """Абстрактный класс для записи, вывода, и удалений с файла"""

    @abstractmethod
    def save_vacancies(self, vacancies):
        pass

    @abstractmethod
    def load_vacancies(self):
        pass

    @abstractmethod
    def delete_vacancies(self):
        pass


class JsonSaver(Json):
    """Класс для записи, вывода, и удалений с файла"""

    def __init__(self, filename=None):
        self.filename = filename

    def save_vacancies(self, vacancies):
        """Метод для записи данных в файл"""
        with open(self.filename, 'w', encoding="utf8") as json_file:
            json.dump(vacancies, json_file, indent=2, ensure_ascii=False)

    def load_vacancies(self):
        """Метод для вывода данных"""
        with open(self.filename, 'r', encoding='utf8') as json_file:
            vacancies = json.load(json_file)
        return vacancies

    def delete_vacancies(self):
        """Метод для удаления данных"""
        with open(self.filename, 'w', encoding='utf8') as json_file:
            json.dump([], json_file)
