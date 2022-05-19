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

def tryer(question, error_message, check_type, req = None):
    while True:
        try:
            result = check_type(input(question))
            if req == None:
                return result
            elif req(result):
                return result
            else:
                print(error_message)
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
    def __init__(self, nr):
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
        customers = db_loader(self.path)
        if str(self.nr) in customers:
            self.load()
            if self.data["code"] == code:
                return self.data
            else:
                return "incorrect code"
        else:
            return "Please enter a valid id!"

class product(main_class):
    def __init__(self, nr):
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