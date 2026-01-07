import json
import os

import requests

from API_manager import HeadHunterAPI

CURRENCY_API_KEY = os.getenv('CURRENCY_API_KEY')


def calc_salary(salary_min: int, salary_max: int, currency: str) -> float:
    """Возвращает среднее значение ЗП, если  определены мин и макс. Если нет - возвращает то, ктр определено"""
    if salary_min == 0:
        return exchange_currency(salary_max, currency)
    elif salary_max == 0:
        return exchange_currency(salary_min, currency)
    else:
        avr_original = (int(salary_min) + int(salary_max)) / 2
        return exchange_currency(avr_original, currency)


def exchange_currency(amount: float, from_: str) -> float:
    """Возвращает размер ЗП с учетом пересчета в рубли по текущему курсу"""
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={from_}&amount={amount}"
    headers = {"apikey": CURRENCY_API_KEY}

    if amount >= 0:
        response = requests.get(url, headers=headers)
        status_code = response.status_code
        data = json.loads(response.text)
        return int(data['result'])
        # if from_ == 'AZN':
        #     return amount * 57.25
        # elif from_ == 'BYR':
        #     return amount * 38.56
        # elif from_ == 'EUR':
        #     return amount * 106.68
        # elif from_ == 'USD':
        #     return amount * 99.25
        # elif from_ == 'GEL':
        #     return amount * 37.37
        # elif from_ == 'KGS':
        #     return amount * 1.11
        # elif from_ == 'KZT':
        #     return amount * 0.22
        # elif from_ == 'RUR':
        #     return amount
        # elif from_ == 'UAH':
        #     return amount * 2.65
        # elif from_ == 'UZS':
        #     return amount * 0.0083


def set_vacancies_list(employers: list) -> tuple[list[tuple], list[tuple]]:
    """Преобразовывает данные, полученные по API и возвращает два списка кортежей:
    с данными по вакансиям и данными по работодателям"""
    vacancies_list = []
    employers_list = []
    for i in HeadHunterAPI().get_vacancies(employers):
        vacancy = [
            int(i['id']),
            i['name'],
            i['area']['name'],
            i['employer']['id'],
            i['alternate_url'],
            int(i['salary']['from']) if i['salary']['from'] else 0,
            int(i['salary']['to']) if i['salary']['to'] else 0,
            i['salary']['currency'],
            calc_salary(
                int(i['salary']['from'] if i['salary']['from'] is not None else 0),
                int(i['salary']['to'] if i['salary']['to'] is not None else 0),
                i['salary']['currency']
            ),
            i['snippet']['responsibility'].strip() if i['snippet']['responsibility'] else None,
            i['snippet']['requirement'].strip() if i['snippet']['requirement'] else None
        ]
        employer = [
            int(i['employer']['id']),
            i['employer']['name'],
            i['employer']['alternate_url'],
            i['employer']['vacancies_url'],
            1 if i['employer']['trusted'] else 0
        ]
        vacancies_list.append(tuple(vacancy))
        employers_list.append(tuple(employer))
    return vacancies_list, list(set(employers_list))
