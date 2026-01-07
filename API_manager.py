import requests


class HeadHunterAPI:
    """Класс для работы с HeadHunter по API.
    Максимальное количество сущностей, выдаваемых API равно 2000 (стр. с 0 по 19 вкл. по 100)"""
    def check_connection(self) -> int:
        """функция для проверки статус-кода при работе с API"""
        response = requests.get('https://api.hh.ru/vacancies')
        return response.status_code

    def get_vacancies(self, employers) -> list:
        """обращается к API и выгружает список вакансии тех компаний, ктр-е указаны в аргументе employers"""
        data = []
        params = {
            'employer_id': employers,
            'per_page': 100,
            'only_with_salary': True,
            'period': 30
        }
        while True:
            raw_data = requests.get('https://api.hh.ru/vacancies', params=params).json()
            page = raw_data['page']
            pages = raw_data['pages']
            data.extend(raw_data['items'])
            if page >= pages - 1:
                break
            params['page'] = page + 1
        return data
