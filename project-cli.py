import datetime
import json

def printUser():
    print("Select type of user: ")
    print("[1] Admin")
    print("[2] Cashier")
    print("[0] Exit")

    choice = input("Enter user: ")

    if choice == "1":
        adminMain()
    elif choice == "2":
        cashierMain()
    elif choice == "0":
        print("Good bye")
        exit()
    else:
        print("Invalid input")

def adminMain():
    while True:
        print("-" * 20 + "ADMIN MENU" + "-" * 20)
        print(f"Time: {datetime.datetime.now()}")

        print("[1] Add movie slot")
        print("[2] Edit movie")
        print("[3] Delete a movie")
        print("[4] View movie/s")
        print("[0] Go back")

        choice = input("Enter choice: ")

        if choice == "1":
            addMovie()
        elif choice == "2":
            editMovie()
        elif choice == "3":
            deleteMovie()
        elif choice == "4":
            viewMovieAdmin()
        elif choice == "0":
            printUser()
        else:
            print("Invalid input")


def cashierMain():
    while True:
        print("-" * 20 + "CASHIER MENU" + "-" * 20)
        print(f"Time: {datetime.datetime.now()}")

        print("[1] View Movies")
        print("[2] Book Movies")
        print("[0] Go back")

        choice = input("Enter choice: ")

        if choice == "1":
            viewMovieCashier()
        elif choice == "2":
            bookMovie()
        elif choice == "3":
            printUser()
        else:
            print("Invalid input")


# admin
def addMovie():
    pass

def editMovie():
    pass

def deleteMovie():
    pass

def viewMovieAdmin():
    pass

# cashier
def viewMovieCashier():
    pass

def bookMovie():
    pass


while True:
    printUser()