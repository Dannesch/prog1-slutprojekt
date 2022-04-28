from main import *
from shutil import get_terminal_size
from reaction import Game

harald = customer(765472)

#print(harald.register("Harald", 10, 4453))

print(harald.login(1234).data)



chips = product(392630)

#print(chips.add_product("Chips", 12, 10, 100))

print(chips.get_data())

columns = get_terminal_size().columns - 2

easy = columns - 1 if columns % 2 == 0 else columns
medium = columns // 2 + 1 if (columns // 2) % 2 == 0 else columns // 2 
hard = columns // 4 + 1 if (columns // 4) % 2 == 0 else columns // 4 
expert = columns // 8 + 1 if (columns // 8) % 2 == 0 else columns // 28

while True:
    marg = 8
    gamemode = int(input("What gamemode do you want?\n\n\t1. Easy \n\t2. Medium \n\t3. Hard \n\t4. Expert \n\t5. Exit \n\n"))

    if gamemode == 1:
        marg /= 1
        difficulty = easy
    elif gamemode == 2:
        marg /= 2
        difficulty = medium
    elif gamemode == 3:
        marg /= 4
        difficulty = hard
    elif gamemode == 4:
        marg /= 8
        difficulty = expert
    else:
        break
    
    hej = Game(4,difficulty,1/100)

    marg -= 1
    hej.change(int(marg), seperator=["v","ᴧ"], eadge=[" "," "], ends=[">","<"], line = "-")

    game = hej.start()

    print("You", "completed" if game else "failed", "the", "easy" if gamemode == 1 else "medium" if gamemode == 2 else "hard" if gamemode == 3 else "expert", "difficulty")