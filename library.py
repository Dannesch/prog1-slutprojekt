import json
import os
import random

db_folder = "data/"
customer_path = db_folder + "customers.json"
product_path = db_folder + "products.json"

def db_loader(db_path):
    if not os.path.exists(db_path):
        with open(db_path, "w") as fp:
            json.dump({}, fp)
            fp.close()
            return {}
    else:
        with open(db_path, "r") as fp:
            return json.load(fp)

def calculate_change(money):
    possible_cash = [1000, 500, 200, 100, 50, 20, 10, 5, 2, 1]
    money = round(money)
    cash = [0]*10
    change = ""
    count = 0
    while count != len(possible_cash):
        if money - possible_cash[count] >= 0:
            cash[count] += 1
            money -= possible_cash[count]
        else:
            count += 1
    for i in range(len(cash)):
        amount = cash[i]
        end = "lapp"
        if i > 6:
                end = "krona"
        if amount > 1:
            if i > 6:
                end = "kronor"
            end = "lappar"
        if amount != 0:
            change += f"{amount}x {possible_cash[i]} {end}, "
    return change[:-2]

def tryer(question, error_message, check_type, req = None, error_message_req = None):
    if error_message_req == None:
        error_message_req = error_message
    while True:
        try:
            result = check_type(input(question))
            if req == None:
                return result
            elif req(result):
                return result
            else:
                print(error_message_req)
        except:
            print(error_message)

def for_tryer(question, error_message, check_type, attempts, req = None, error_message_req = None):
    if error_message_req == None:
        error_message_req = error_message
    for i in range(attempts):
        try:
            result = check_type(input(question))
            if req == None:
                return result
            elif req(result):
                return result
            else:
                print(error_message_req)
        except:
            print(error_message)

def database_searcher(path, name):
    database = db_loader(path)
    for i in database:
        if database[i]['name'] == name.capitalize():
            return i


class main_class:
    def save(self):
        content = db_loader(self.path)
        content[self.nr] = self.data
        with open(self.path,"w") as fp:
            json.dump(content, fp)

    def load(self):
        self.data = db_loader(self.path)[self.nr]

    def edit(self, item, value):
        self.load()
        self.data[item] = value
        self.save()

class customer(main_class):
    def __init__(self, nr = 0):
        self.nr = str(nr)
        self.path = customer_path

    def register(self, name, age, code, credit = 0, purchases = 0):
        self.nr = str(random.randint(100000, 999999))
        customers = db_loader(self.path)
        while str(self.nr) in customers:
            self.nr = str(random.randint(100000, 999999))
        self.data = {
            "name": name.capitalize(),
            "age": age,
            "credit": credit,
            "purchases": purchases,
            "code": code
        }
        self.save()
        return f"Registration completed, your id is {self.nr}"

    def login(self, code):
        self.load()
        if self.data["code"] == code:
            return self.data
        else:
            return False

class product(main_class):
    def __init__(self, nr = 0):
        self.nr = str(nr)
        self.path = product_path

    def add_product(self, name, cost, weight, amount, sold = 0, sale = 0):
        self.nr = str(random.randint(100000, 999999)) #ta input för sträckkod och gör felhantering för om det är fel längd
        products = db_loader(self.path)
        while str(self.nr) in products:
            self.nr = str(random.randint(100000, 999999))
        self.data = {
            "name": name.capitalize(),
            "cost": cost,
            "weight": weight,
            "amount": amount,
            "sold": sold,
            "sale": sale
        }
        self.save()
        return f"Product added, the product id is {self.nr}"

    def get_data(self):
        self.load()
        return self.data

#######################################################################################################