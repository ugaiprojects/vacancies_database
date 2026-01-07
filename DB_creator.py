import sqlite3

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql
from utils import set_vacancies_list


def create_database(database, password):
    """Фунуция для создания БД с названием аргумента database"""
    connection = psycopg2.connect(host='localhost', database='postgres', user='postgres', password=password)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = connection.cursor()
    try:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database)))
        print(f'База данных {database} создана')
    except sqlite3.DatabaseError as error:
        print("Error: ", error)


class DBcreator:
    """Класс для работы с БД: создание таблиц и заполнение их данными"""

    def __init__(self, password, database, vacancies_table, employers_table, employers):
        self.connection = psycopg2.connect(host='localhost', database=database, user='postgres', password=password)
        self.vacancies_table = vacancies_table
        self.employers_table = employers_table
        self.vacancies, self.employers = set_vacancies_list(employers)

    def create_vacancies_table(self) -> None:
        """Создает таблицу для работы с вакансиями"""
        with self.connection.cursor() as cursor:
            try:
                cursor.execute("""CREATE TABLE {} (
                                                   vacancy_id serial PRIMARY KEY,
                                                   hh_vacancy_id int NOT NULL,
                                                   title varchar NOT NULL,
                                                   area varchar NOT NULL,
                                                   employer_id int NOT NULL,
                                                   url varchar NOT NULL,
                                                   salary_min int,
                                                   salary_max int,
                                                   currency varchar,
                                                   salary_avr_rub int,
                                                   description varchar,
                                                   requirements varchar
                                                   );""".format(self.vacancies_table)
                               )
                print(f'Таблица {self.vacancies_table} создана')
            except sqlite3.DatabaseError as error:
                print("Error: ", error)

    def create_employers_table(self) -> None:
        """Создает таблицу для работы с компаниями-работодателями"""
        with self.connection.cursor() as cursor:
            try:
                cursor.execute("""CREATE TABLE {} (
                                                   employer_id serial PRIMARY KEY,
                                                   title varchar NOT NULL,
                                                   url varchar NOT NULL,
                                                   vacancies_url varchar NOT NULL,
                                                   trusted int NOT NULL,
                                                   CONSTRAINT chk_trusted CHECK (trusted IN (1, 0))
                                                   );""".format(self.employers_table)
                               )
                print(f'Таблица {self.employers_table} создана')
            except sqlite3.DatabaseError as error:
                print("Error: ", error)

    def fill_in_vacancies(self) -> None:
        """заполняет таблицу данными о вакансиях"""
        with self.connection.cursor() as cursor:
            try:
                cursor.executemany("""INSERT into {} (
                                                      hh_vacancy_id, 
                                                      title, 
                                                      area, 
                                                      employer_id, 
                                                      url, 
                                                      salary_min, 
                                                      salary_max, 
                                                      currency, 
                                                      salary_avr_rub, 
                                                      description, 
                                                      requirements
                                                      ) 
                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(self.vacancies_table),
                                   self.vacancies
                                   )
                print(f'Таблица {self.vacancies_table} заполнена данными')
            except sqlite3.DatabaseError as error:
                print("Error: ", error)

    def fill_in_employers(self) -> None:
        """заполняет таблицу данными о компаниях-работодателях"""
        with self.connection.cursor() as cursor:
            try:
                cursor.executemany("""INSERT into {} (
                                                      employer_id, 
                                                      title, 
                                                      url, 
                                                      vacancies_url, 
                                                      trusted
                                                      ) 
                                   VALUES (%s, %s, %s, %s, %s)""".format(self.employers_table),
                                   self.employers
                                   )
                print(f'Таблица {self.employers_table} заполнена данными')
            except sqlite3.DatabaseError as error:
                print("Error: ", error)
