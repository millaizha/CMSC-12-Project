import datetime

def printUser(movies):
    print("Select type of user: ")
    print("[1] Admin")
    print("[2] Cashier")
    print("[0] Exit")

    choice = input("Enter user: ")

    if choice == "1":
        adminMain(movies)
    elif choice == "2":
        cashierMain()
    elif choice == "0":
        print("Good bye")
        exit()
    else:
        print("Invalid input")

def adminMain(movies):
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
            addMovie(movies)
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
def addMovie(movies):
    with open("movies.txt", "r") as f:
        intMovieID = int(f.readline()) + 1
    strMovieID = str(intMovieID).zfill(4) # str kasi hindi kaya mag 4 digit if int
    

    name = input("Enter Movie Name: ")
    genre = input("Enter Genre: ")
    restrict = input("Enter Movie Restriction [G | PG | RPG | R18+]: ")
    venue = input("Enter Cinema Venue [1 | 2 | 3]: ")
    startDate = input("Enter start date: [mm/dd/yy]: ")
    endDate = input("Enter end date: [mm/dd/yy]: ")
    startTime = input("Enter start time: [HH:MM (24)]: ")
    endTime = input("Enter end time: [HH:MM (24)]: ")

    movies[strMovieID] = [name, genre, restrict, venue, startDate, endDate, startTime, endTime]

    print(strMovieID, movies[strMovieID])

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

movies = {}

while True:
    printUser(movies)