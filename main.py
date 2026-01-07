import os

from DB_creator import DBcreator, create_database
from DB_manager import DBManager

employers = [
    1212374, 847383, 2661787, 9804951, 598471, 8966021, 851604, 1818108,
    4574784, 9056925, 56119, 2498826, 4080, 5269493, 5473303, 113953
]
sql_database = 'NEW'
sql_password = os.getenv('POSTGRES_PASSWORD')
sql_vacancies_table = 'vacancies_NOV'
sql_employers_table = 'employers_NOV'

# создали БД
create_database(sql_database, sql_password)

# активировали класс для работы БД
HH_database = DBcreator(sql_password, sql_database, sql_vacancies_table, sql_employers_table, employers)

# активировали соединение
with HH_database.connection:
    # создали таблицы
    HH_database.create_vacancies_table()
    HH_database.create_employers_table()

    # заполнили таблицы
    HH_database.fill_in_vacancies()
    HH_database.fill_in_employers()

# закрыли соединение
HH_database.connection.close()

# начали работу в самой БД, активировали дочерний класс
query = DBManager(sql_password, sql_database, sql_vacancies_table, sql_employers_table, employers)

# открыли соединение
with query.connection:
    query.get_companies_and_vacancies_count()
    query.get_all_vacancies()
    query.get_avg_salary()
    query.get_vacancies_with_higher_salary()
    query.get_vacancies_with_keyword('python')

# закрыли соединение
query.connection.close()
