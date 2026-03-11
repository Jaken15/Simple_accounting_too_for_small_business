import os
import sqlite3
import sys

def get_db_path():

    if getattr(sys,'frozen',False): # check kung exe ba yung file
        base_path = os.path.dirname(sys.executable) # kung exe gagawa ng path para sa exe
    else:
        base_path = os.path.abspath('.') # kung script naman ito ang path
    db_folder_path = os.path.join(base_path,"Database folder")
    database_path = os.path.join(db_folder_path,'My_database.db') # gagawa ng database file
    if not os.path.exists(db_folder_path): # kung wala pang database folder gagawa ng folder
        os.makedirs(db_folder_path)
        sqlite3.connect(database_path)
    return database_path

class My_database:
    def __init__(self):
        self.database_path = get_db_path() 
        self.Create_table()
    def Create_table(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS my_database(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           amount INTEGER,
                           type TEXT,
                           category TEXT,
                           date TEXT
                           )""")
            cursor.execute("SELECT id FROM my_database")
            if len(cursor.fetchall()) == 0:
                cursor.execute("INSERT INTO my_database (id) VALUES (1000)")
            conn.commit()

    def get_all_date(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT date FROM my_database WHERE date IS NOT NULL ")
            return cursor.fetchall()
    def get_all_data_by_date(self,start_date,end_date):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            try:
                query = """
                SELECT * FROM my_database 
                WHERE date BETWEEN ? AND ?
                """
                cursor.execute(query,(start_date,end_date))
                return cursor.fetchall()
            except Exception as e:
                print(e)

    def get_sum_of_category(self,category,start_date,end_date):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                SELECT SUM(amount) FROM my_database
                WHERE type = 'expense' AND category = ?
                AND date BETWEEN ? AND ?
            """,(category,start_date,end_date))
                return cursor.fetchall()
            except Exception as e:
                print(e)

    def insert_data(self,amount,type,category,date):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO my_database (amount,type,category,date) VALUES (?,?,?,?)",(amount,type,category,date))
                conn.commit()
            except Exception as e:
                print(e)
    
    def get_all_data(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM my_database")
                return cursor.fetchall()
            except Exception as e:
                print(e)

    def get_all_data_by_category(self,category):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM my_database WHERE category = ?",(category,))    
                return cursor.fetchall()
            except Exception as e:
                print(e)
    
    def get_amount_by_date(self,type,start_date,end_date):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                               SELECT SUM(amount) FROM my_database
                               WHERE type = ? AND date BETWEEN ? AND ?
                              """,(type,start_date,end_date))
                return cursor.fetchall()
            except Exception as e:
                print(e)

    def delete_data(self,id):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""DELETE FROM my_database
                               WHERE id = ?
                               """,(id,))
                print("success")
                conn.commit()
            except Exception as e:
                print(e)

    def update_data(self,category,id):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""UPDATE my_database
                               SET category = ?
                               WHERE id = ?
                                """,(category,id))
            except Exception as e:
                print(e)

    def get_categories(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT DISTINCT category FROM my_database WHERE category IS NOT NULL ORDER BY category ASC;")
                return cursor.fetchall()
            except Exception as e:
                print(e)

    def read_table(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            print(cursor.fetchall())

    def get_expenses_and_category(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                               SELECT category, SUM(amount)
                               AS total_amount
                               FROM my_database
                               WHERE type = 'expense'
                               AND category IS NOT NULL
                               GROUP BY category
                               ORDER BY amount ASC;
                               """)
                return cursor.fetchall()
            except Exception as e:
                print(e)           

    def get_dynamic_data(self,type=None,category=None,start_date=None,end_date=None):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            try:
                query = "SELECT * FROM my_database WHERE 1=1"
                params = []

                if type:
                    query += " AND type = ?"
                    params.append(type)

                if category:
                    query += " AND category = ?"
                    params.append(category)

                if start_date and end_date:
                    query += " AND date BETWEEN ? AND ?"
                    params.extend([start_date,end_date])
                
                query += " ORDER BY category ASC;"

                tuple_params = tuple(params)
                cursor.execute(query,tuple_params)

                return cursor.fetchall()
            except Exception as e:
                print(e)
                return []
        
    def get_all_amount(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                               SELECT 
                               SUM(CASE WHEN type='income' THEN amount ELSE 0 END) AS total_income,
                               SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) AS total_expense
                               FROM my_database
                               """)
                total_income,total_expense = cursor.fetchone()
                amount = [total_income,total_expense]
                return amount
                
            except Exception as e:
                print("Error from get all amount ",e)
    
db = My_database()
type = "expense"
category = "Movie"
start_date = '2026-01-31'
end_date = '2026-02-02'

# db.get_filter_data(type,category,start_date,end_date)
# db.get_dynamic_data(type,category,start_date,end_date)
# db.get_dynamic_data(start_date='2026-02-02',end_date='2026-02-02')
# db.get_dynamic_data(startdate='2026-02-01')
# db.get_dynamic_data(enddate='2026-02-04')
