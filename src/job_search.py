from abc import ABC, abstractmethod
from http import HTTPStatus

import requests
import json


class VacanciesAPI(ABC):
    """Абстрактный класс для платформ HeadHunter, SuperJob для получение API"""

    @abstractmethod
    def get_vacancies(self, params):
        pass


class HeadHunterAPI(VacanciesAPI):
    """Класс для получения API с платформы HeadHunter"""
    api_hh = 'https://api.hh.ru/vacancies?text='

    def __init__(self):
        self.items_hh = None

    def get_vacancies(self, params: str):
        """Получение заданных пользователем профессий с платформы HeadHunter"""
        response = requests.get(f'{self.api_hh}{params}')
        if not response.status_code == HTTPStatus.OK:
            return f"Ошибка! {response.status_code}"
        self.items_hh = response.json()
        return self.items_hh


class SuperJob(VacanciesAPI, ABC):
    """"Класс для получения API с платформы SuperJob"""
    api_sj = "https://api.superjob.ru/2.0/vacancies/"

    def __init__(self):
        self.items_sj = None

    def get_vacancies(self, params: str):
        """Получение заданных пользователем профессий с платформы SuperJob"""
        headers = {
            "X-Api-App-Id": 'v3.r.137643549.5dafea9523d8382ad2dd0791d3bb597bb32e4eff'
                            '.6b545afc3b70eeeb7093cd923f7dc0f8b147f2cb'
        }
        params = {
            "keyword": "Python",
            "page": "1"
        }
        response = requests.get(self.api_sj,
                                params=params,
                                headers=headers)
        if not response.status_code == HTTPStatus.OK:
            return f'Ошибка! Статус: {response.status_code}!'
        self.items_sj = response.json()
        return self.items_sj


class Vacancies:
    """Класс для работы с вакансиями"""

    def __init__(self, name, url, salary, skills):
        """Инициализация вакансий по заданным атрибутам"""
        try:
            self.name = name
            self.url = url
            self.salary = salary
            self.skill = skills
        except AttributeError:
            raise AttributeError(
                "Введите название вакансии, ссылка на вакансию, зарплата, краткое описание и требования")

    def __lt__(self, other):
        return self.salary < other.salary

    def __gt__(self, other):
        return self.salary > other.salary


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
            json.dump(vacancies, json_file)

    def load_vacancies(self):
        """Метод для вывода данных"""
        with open(self.filename, 'r', encoding='utf8') as json_file:
            vacancies = json.load(json_file)
        return vacancies

    def delete_vacancies(self):
        """Метод для удаления данных"""
        with open(self.filename, 'w', encoding='utf8') as json_file:
            json.dump([], json_file)
