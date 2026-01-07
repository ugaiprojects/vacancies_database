from DB_creator import DBcreator


class DBManager(DBcreator):
    """Класс для работы с БД: сортировки, фильтрации и тд. Дочерний от DBcreator"""

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                           """SELECT {0}.title, COUNT (*)
                           FROM {1}
                           JOIN {0} USING (employer_id)
                           GROUP BY {0}.title;""".format(self.employers_table, self.vacancies_table)
                           )
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты, региона и ссылки на вакансию"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                           """SELECT {0}.title as company_title, {1}.title, 
                           {1}.salary_avr_rub, {1}.area, 
                           {1}.url
                           FROM {1}
                           JOIN {0} USING (employer_id)
                           ORDER BY {1}.salary_avr_rub DESC;""".format(self.employers_table, self.vacancies_table)
                           )
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                           """SELECT AVG(salary_avr_rub)
                           FROM {};""".format(self.vacancies_table)
                           )
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                           """SELECT {0}.title as company_title, {1}.* 
                           FROM {1}
                           JOIN {0} USING (employer_id) 
                           WHERE salary_avr_rub > (SELECT AVG(salary_avr_rub) FROM {1})
                           ORDER BY salary_avr_rub DESC;""".format(self.employers_table, self.vacancies_table)
                           )
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    def get_vacancies_with_keyword(self, key):
        """получает список всех вакансий, в названии которых содержатся переданные
        в метод слова, например “python” без учета регистра"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                           """SELECT {0}.title as company_title, {1}.* 
                           FROM {1}
                           JOIN {0} USING (employer_id) 
                           WHERE lower({1}.title) LIKE '%{2}%'
                           ORDER BY salary_avr_rub DESC;"""
                           .format(self.employers_table, self.vacancies_table, key.lower())
                           )
            rows = cursor.fetchall()
            for row in rows:
                print(row)
