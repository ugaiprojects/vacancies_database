# Script for extracting job vacancies data from "HeadHunter" platform into Postgres DB and its filtering and sorting upon the user's query


# For working with DB the users needs:
* DB name,
* id of chosen companies
* authorization details (Postgres, https://apilayer.com/) 
* Table name for vacancies
* Table name for companies


# Functions:

* functions for working with API is executed in API_manager.py
* for creating and filling in the tables a separate Class was developed within DB_creator.py
* sorting, filtering functions are performed within the class in DB_manager.py
* additional functions for reformatting the data, calculating the currency exchange rates are executed within utils.py

# Notes:
* data retrieval is subject to the limits set by HeadHunter platform - 2000 vacancies
* data is dowloaded in DB in accordance to the current currency exchange rate via https://apilayer.com/





# Программа, реализующая выгрузку данных с платформы "HeadHunter" в базу данных Postgres и их фильтрацию/сортировку по запросу



# Для работы с БД пользователю необходимо указать:
* наименование БД,
* id выбранных для анализа компаний-работодателей
* данные для авторизации (Postgres, https://apilayer.com/) 
* наименование таблицы для выгрузки данных по вакансиям 
* наименование таблицы для выгрузки данных по компаниям-работодателям 


# Функционал:

* функционал для работы с API реализован в API_manager.py
* для создания и заполнения таблиц реализован класс в рамках DB_creator.py
* функционал по сортировке, фильтрации, выборке данных реализован в классе в рамках DB_manager.py
* вспомогательный функционал по форматированию данных, пересчетов курса валюты реализован в utils.py

# Прим:
* Выгрузка осуществляется с учетом ограничений по количеству вакансий - 2000
* В БД осуществляется выгрузка данных с учетом пересчета ЗП по текущему курсу валюты вакансии к рублю через https://apilayer.com/
