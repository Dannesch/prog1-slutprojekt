import json
import os
import random

customer_path = "customers.json"
product_path = "products.json"

def db_loader(db_path):
    if not os.path.exists(db_path):
        with open(db_path, "w") as fp:
            json.dump({}, fp)
            fp.close()
            return {}
    else:
        with open(db_path, "r") as fp:
            return json.load(fp)

class main_class:
    def save(self):
        cont = db_loader(self.path)
        cont[self.nr] = self.data
        with open(self.path,"w") as fp:
            json.dump(cont, fp)
    def load(self):
        self.data = db_loader(self.path)[self.nr]


class customer(main_class):
    def __init__(self, nr):
        self.nr = str(nr)
        self.path = customer_path

    def register(self, name, age, code):
        self.nr = str(random.randint(100000, 999999))
        customers = db_loader(self.path)
        while str(self.nr) in customers:
            self.nr = str(random.randint(100000, 999999))
        self.data = {
            "name": name,
            "age": age,
            "credit": 0,
            "purchases": 0,
            "code": code
        }
        self.save()
        return f"Registration completed, your id is {self.nr}"

    def login(self, code):
        customers = db_loader(self.path)
        if str(self.nr) in customers:
            self.load()
            if self.data["code"] == code:
                return self
            else:
                return "incorrect code"
        else:
            return "Please enter a valid id!"

class product(main_class):
    def __init__(self, nr):
        self.nr = str(nr)
        self.path = product_path
    
    def add_product(self, name, weight, cost, amount, sale = 0):
        pass
        


#######################################################################################################