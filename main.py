from library import *

requierment = lambda x: 1<=x<=2
requierment_yn = lambda x: x.lower() == "j" or x.lower() == "n"
error_message = "Var god välj ett av alternativen!"

def cashier():
    products = []
    while True:
        done = False
        product_db = db_loader(product_path)

        name = input("Vilken produkt vill du köpa?\n")

        if not name.isnumeric():
            nr = database_searcher(product_path, name)
        else:
            nr = int(name)
            if nr not in product_db:
                nr = None
            else:
                name = product_db[nr]['name']

        if nr == None:
            print("Produkten finns inte!")
        else:
            selected_product = product(nr)
            data = selected_product.get_data()
            amount = data['amount']

            for i, j in products:
                if i == nr:
                    if tryer(f"Vill du ändra mängden {name} du köper? (j/n)\n", error_message, str, requierment_yn).lower() == "j":
                        requested_amount = tryer(f"Hur många vill du ha?\n", "Var god välj ett tal!", int, lambda x: 0 <= x <= amount, f"Det finns bara {data['amount']} {name}!")
                        if requested_amount != 0:
                            products[products.index([i,j])] = [i, requested_amount]
                        else:
                            del products[products.index([i,j])]
                        done = True

            if done:
                pass
            elif amount == 0:
                print(f"Det är slut på {name}!")
            else:
                sale = data['sale']
                cost = data['cost']
                if sale != 0:
                    print(f"\nProduket är på rea!")
                    print(f"Produkten kostar: {round(data['cost'] * sale, 2)}kr! Spara {int((1 - sale) * 100)}%")
                    print(f"Ordenarie pris: {cost}kr\n")
                else:
                    print(f"Produkten kostar: {cost}kr")
                requested_amount = tryer(f"Hur många vill du ha?\n", "Var god välj ett tal!", int, lambda x: x <= amount, f"Det finns bara {data['amount']} {name}!")
                products.append([nr, requested_amount])

        total = 0
        total_sale = 0
        print("\nVarukorg:")
        for i,j in products:
            item = product_db[i]
            sale = item['sale']
            cost = item['cost'] * j

            if sale != 0:
                regular_cost = cost
                cost *= sale
                cost = round(cost, 2)
                total_sale += regular_cost - cost

            print(f"{j}x {item['name']}\t{cost}kr")
            total += cost
        print(f"Summa: {total}kr")
        print(f"Du sparar: {total_sale}kr")

        if tryer("\nÄr det allt? (j/n)\n", error_message, str, requierment_yn).lower() == "j":
            break
    
    handeld = customer_handler()
    payment_credit = handeld[0]
    member = handeld[1]

    if payment_credit:
        credit = member.data['credit']
        if credit < total:
            if tryer("Du har inte tillräckligt mycket kredit! Vill du byta till kort/kontant? (j/n)\n", error_message, str, requierment_yn).lower() == "n":
                return
            payment_credit = False
        else:
            credit -= total
            credit = round(credit, 2)
            member.edit('credit', credit)
            print(f"Du har {credit}kr kvar på kontot")

    if not payment_credit:
        if tryer("Vill du betala med kontanter? (j/n)\n", error_message, str, requierment_yn).lower() == "j":
            print(calculate_change(total))
    
    for i, j in products:
        item = product(i)
        item.edit("amount", item.get_data()['amount'] - j)
        item.edit("sold", item.get_data()['sold'] + 1)
    if member != None:
        member.edit("purchases", member.data['purchases'] + 1)


def customer_handler():
    member = None
    customer_db = db_loader(customer_path)
    while True:
        if tryer("Är du medlem? (j/n)\n", error_message, str, requierment_yn).lower() == "j":
            member_id = str(for_tryer("Vad är ditt medlems id? (6-siffrigt)\n", "Ange ett giltigt id!", int, 3, lambda x: 100000 <= x <= 999999 and str(x) in customer_db))
            if member_id != None:
                member = customer(member_id)
                pin = for_tryer("Ange din pinkod\n", "Ange en giltig pinkod!", int, 3, lambda x: member.login(x) != False)
        else:
            if tryer(f"Vill du bli medlem? (j/n)\n", error_message, str, requierment_yn).lower() == "j":
                name = input("Ange namn\n")
                age = tryer("Ange ålder\n", "Var god ange ett tal!", int)
                pin = tryer("Ange en pinkod\n", "Var god ange ett tal!", int)
                member = customer()
                member.register(name, age, pin)
                print(f"Din id är: {member.nr}")
            else:
                return [False, member]

        data = member.login(pin)
        if tryer(f"Hej {data['name']}! Vill du betala med kontokredit? (j/n)\n", error_message, str, requierment_yn).lower() == "j":
            return [True, member]
        else:
            break

    return [False, member]

def inventory():
    database_type = tryer("Vilken databas vill du ändra på? (1 = produkter, 2 = medlemmar)\n", error_message, int, requierment)

    if database_type == 1:
        path = product_path
        database_type_name = "produkt"
    else:
        path = customer_path
        database_type_name = "medlem"

    name = input(f"Vilken {database_type_name} vill du redigera?\n")
    if not name.isnumeric():
        nr = database_searcher(path, name)
    else:
        nr = int(name)
        if nr not in db_loader(path):
            nr = None

    if nr == None:
        create_new = tryer(database_type_name.capitalize() + "en existerar inte, vill du skapa en ny? (j/n)\n", error_message, str, requierment_yn).lower()
        if create_new == "j":
            if name.isnumeric():
                name = input(f"Vad ska {database_type_name}en heta?\n")
            if database_type == 1:
                cost = tryer("Hur mycket kostar produkten?\n", "Var god välj ett tal!", float)
                weight = tryer("Hur mycket väger produkten? (gram)\n", "Var god välj ett tal!", int)
                amount = tryer("Hur många produkter har vi?\n", "Var god välj ett tal!", int)
                sale = tryer(f"Vill du att produkten ska vara på rea? (j/n)\n", error_message, str, requierment_yn).lower()
                if sale == "j":
                    sale = tryer("Hur många procent ska rean vara på? (ex. 0.5 for 50%)\n", "Var god välj en förendrings faktor!", float)
                else:
                    sale = 0.0
                item = product()
                item.add_product(name, cost, weight, amount, sale=sale)
            else:
                age = tryer("Hur gammal är medlemmen?\n", "Var god välj ett tal!", int)
                code = tryer("Vilken kod ska medlemmen ha?\n", "Var god välj ett tal!", int)
                item = customer()
                item.register(name, age, code)

            print(f"{database_type_name.capitalize()}ens id är {item.nr}")
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