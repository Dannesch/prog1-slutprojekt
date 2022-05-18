from main import *

def cashier():
    pass

def inventory():
    pass

system = tryer("Vilket system vill du använda? (1 = kassa, 2 = inventering)\n", "Var god välj ett av alternativen!", int, lambda x: 1<=x<=2)

if system == 1:
    print("Kassa")
else:
    print("Inventering")