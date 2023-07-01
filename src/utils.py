def filter_vacancies(hh_vacancies: list, superjob_vacancies: list, filter_words: str) -> list:
    """ Создание списка вакансий
    """
    hh_list = []
    for vacancies_hh in hh_vacancies:
        if filter_words.lower() in vacancies_hh["name"].lower():
            if vacancies_hh['salary'] is not None:
                if vacancies_hh['salary']["from"] is None:
                    hh_list.append(f"{vacancies_hh['name']}\n"
                                   f"Заработная плата: {vacancies_hh['salary']['to']} {vacancies_hh['salary']['currency']}\n"
                                   f"Опыт работы: {vacancies_hh['experience']['name']}\n"
                                   f"Ссылка на вакансию: {vacancies_hh['alternate_url']}\n")
                elif vacancies_hh['salary']["to"] is None:
                    hh_list.append(f"{vacancies_hh['name']}\n"
                                   f"Заработная плата: {vacancies_hh['salary']['from']} {vacancies_hh['salary']['currency']}\n"
                                   f"Опыт работы: {vacancies_hh['experience']['name']}\n"
                                   f"Ссылка на вакансию: {vacancies_hh['alternate_url']}\n")
                else:
                    hh_list.append(f"{vacancies_hh['name']}\n"
                                   f"Заработная плата: {vacancies_hh['salary']['from']} - {vacancies_hh['salary']['to']} {vacancies_hh['salary']['currency']}\n"
                                   f"Опыт работы: {vacancies_hh['experience']['name']}\n"
                                   f"Ссылка на вакансию: {vacancies_hh['alternate_url']}\n")
            else:
                hh_list.append(
                    f'{vacancies_hh["name"]}\n'
                    f'Заработная плата: по результатам собеседования.\n'
                    f'Требуемый опыт: {vacancies_hh["experience"]["name"]}\n'
                    f'Ссылка на вакансию: {vacancies_hh["alternate_url"]}\n')
    sj_list = []
    for vacancies_sj in superjob_vacancies:
        if filter_words.lower() in vacancies_sj['profession'].lower():
            if vacancies_sj['payment_from'] == 0:
                sj_list.append(f"{vacancies_sj['profession']}\n"
                               f"Заработная плата: {vacancies_sj['payment_to']}\n"
                               f"Опыт работы: {vacancies_sj['experience']['title']}\n"
                               f"Ссылка на вакансию: {vacancies_sj['link']}\n")
            elif vacancies_sj['payment_to'] == 0:
                sj_list.append(f"{vacancies_sj['profession']}\n"
                               f"Заработная плата: {vacancies_sj['payment_from']}\n"
                               f"Опыт работы: {vacancies_sj['experience']['title']}\n"
                               f"Ссылка на вакансию: {vacancies_sj['link']}\n")
            else:
                sj_list.append(f"{vacancies_sj['profession']}\n"
                               f"Заработная плата: {vacancies_sj['payment_from']} - {vacancies_sj['payment_to']}\n"
                               f"Опыт работы: {vacancies_sj['experience']['title']}\n"
                               f"Ссылка на вакансию: {vacancies_sj['link']}\n")
    vacancies = []
    vacancies.extend(sj_list)
    vacancies.extend(hh_list)
    return vacancies


def sort_vacancies(vacancies: list):
    """ Сортировка вакансий"""
    return sorted(vacancies)


def get_top_vacancies(vacancies: list, top_n: int):
    """Первые указанные топ вакансий"""
    return vacancies[:top_n + 1]


def print_vacancies(vacancies: list):
    """Вывод вакансий"""
    for vacancy in vacancies:
        print(vacancy)
        print()
