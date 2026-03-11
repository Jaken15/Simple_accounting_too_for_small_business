from DataBase_path import My_database as database
from datetime import datetime,timedelta

class valid_date:
    def __init__(self):
        self.Database = database()
        self.date_today = datetime.today().strftime("%Y-%m-%d")
          
    def add_data_by_category(self,amount,type,category): #purpose of this function
        # To add the data to database
        try:
            amount_expenses = int(amount)
            self.Database.insert_data(amount_expenses,type,category,self.date_today)
        except Exception as e:
            print("Error from add expense by category",e)

    def recent_category_expenses(self): # the for purpose of this function
        # To get the latest expenses base on category
        try:
            start_date = self.date_today
            end_date = self.date_today
            category_expenses = []
            recent_expenses_by_category = self.Database.get_expenses_and_category()
            for category in recent_expenses_by_category:
                category_expenses.append(category)
            return category_expenses
        except Exception as e:
            print("Error from category expenses",e)
        
    def recent_data(self): # purpose of this function is to get all the 
        # data from database from date today
        try:
            recent_data = self.Database.get_all_data_by_date(self.date_today,self.date_today)
            return recent_data
        except Exception as e:
            print("Error from recent data",e)

    def all_data(self):
        try:
            record_of_all_data = self.Database.get_all_data()
            return record_of_all_data
        except Exception as e:
            print("Error from all data")
    
    def current_balance(self):
        try:
            balance = self.total_expense - self.total_income
            if balance == None:
                balance = 0
            return balance
        except Exception as e:
            print("error from current balance")

    def list_of_date(self):
        date_list = []
        database_date = self.Database.get_all_date()
        for date in database_date:
            date_list.append(date[0])
        return date_list
    
    def categories(self):
        category_list = []
        try:
            for categories in self.Database.get_categories():
                for c in categories:
                    category_list.append(c)
            return category_list
        except Exception as e:
            print("error from categories",e)
        
    def filter_data(self,type,category,start_date,end_date):
        try:
            if type == "all":
                type = ""
            data = self.Database.get_dynamic_data(type,category,start_date,end_date)
            return data
        except Exception as e:
            print("error from filter data",e)

    def balance_income_expense(self):
        try:
            amount = self.Database.get_all_amount()
            current_balance = amount[1] - amount[0]
            if current_balance < 0:
                current_balance = 0
            amount.append(current_balance)
            return amount
        except Exception as e:
            print(e)

testing = valid_date()
# print(testing.balance_income_expense())