from main import *

requierment = lambda x: 1<=x<=2
error_message = "Var god välj ett av alternativen!"

def cashier():
    pass

def inventory():
    database_type = tryer("Vilken databas vill du ändra på? (1 = produkter, 2 = medlemmar)\n", error_message, int, requierment)
    
    if database_type == 1:
        path = product_path
        database_type_name = "produkt"
    else:
        path = customer_path
        database_type_name = "medlem"
    
    name = input(f"Vilken {database_type_name} vill du redigera?\n")
    nr = database_searcher(path, name)
    if nr == None:
        create_new = tryer(database_type_name.capitalize() + "en existerar inte, vill du skapa en ny? (j/n)\n", error_message, str, lambda x: x.lower() == "j" or x.lower() == "n")
        if create_new == "y":
            if database_type == 1:
                cost = tryer("Hur mycket kostar produkten?\n", "Var god välj ett tal!", int)
                weight = tryer("Hur mycket väger produkten?\n", "Var god välj ett tal!", int)
                amount = tryer("Hur många produkter har vi?\n", "Var god välj ett tal!", int)
                product().add_product(name, cost, weight, amount, sale=sale)
            else:
                item = customer().register
            

    else:
        if database_type == 1:
            item = product(nr)
        else:
            item = customer(nr)
        
        item.load()
        editable_items = "("
        for i in item.data:
            editable_items += i + ", "
        editable_items = editable_items[:-2]
        editable_items += ")"

        edit_value = tryer(f"Vad vill du redigera? {editable_items}\n", error_message, str, lambda x: x in editable_items)
        value = tryer("Vad vill du ändra det till?\n", error_message, type(item.data[edit_value]))
        item.edit(edit_value, value)


system = tryer("Vilket system vill du använda? (1 = kassa, 2 = inventering)\n", error_message, int, requierment)

if system == 1:
    cashier()
else:
    inventory()