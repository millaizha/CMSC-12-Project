import datetime
import ast

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
        print("[5] Go back")
        print("[0] Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            addMovie(movies)
        elif choice == "2":
            editMovie(movies)
        elif choice == "3":
            deleteMovie(movies)
        elif choice == "4":
            viewMovieAdmin()
        elif choice == "5":
            printUser()
        elif choice == "0":
            print("Good bye")
            exit()
        else:
            print("Invalid input")


def cashierMain():
    while True:
        print("-" * 20 + "CASHIER MENU" + "-" * 20)
        print(f"Time: {datetime.datetime.now()}")

        print("[1] View Movies")
        print("[2] Book Movies")
        print("[3] Go back")
        print("[0] Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            viewMovieCashier()
        elif choice == "2":
            bookMovie()
        elif choice == "3":
            printUser()
        elif choice == "0":
            print("Good bye")
            exit()
        else:
            print("Invalid input")


# admin
def addMovie(movies):
    with open("movies.txt", "r") as f:
        intMovieID = int(f.readline()) + 1

    MovieID = str(intMovieID).zfill(4) # str because int cannot have a 4 0s 
    
    name = input("Enter Movie Name: ")
    genre = input("Enter Genre: ")
    restrict = input("Enter Movie Restriction [G | PG | RPG | R18+]: ")
    venue = input("Enter Cinema Venue [1 | 2 | 3]: ")
    date = input("Enter Date [mm/dd/yy]: ")
    startTime = input("Enter start time: [HH:MM (24)]: ")
    endTime = input("Enter end time: [HH:MM (24)]: ")
    price = int(input("Enter price: "))

    movies[MovieID] = [name, genre, restrict, venue, date, startTime, endTime, price]

    with open("movies.txt", "w") as f:
        f.write(str(intMovieID))
        print("\n", movies, file = f)

def editMovie(movies):
    print("Movie List")
    for k, v in movies.items():
        print(k, "-", v[0])

    movieID = input("Enter Movie ID to edit [0 to cancel]: ")

    if movieID in movies:
        print("[1] Edit 1 detail")
        print("[2] Edit whole details")
        print("[3] Go back to ID selection")

        choice = input("Enter choice: ")

        if choice == "1":
            editOneDetail(movies, movieID)
        elif choice == "2":
            editAllDetails(movies, movieID)
        elif choice == "3":
            editMovie(movies)
        else:
            print("Invalid input")
    elif movieID == "0":
        adminMain(movies)
    else:
        print(f"{movieID} is not in the movie list.")

def editOneDetail(movies, movieID):
    info = movies[movieID]
    
    print(f"Movie {movieID} Details:")
    print(f"[1] Name: {info[0]}")
    print(f"[2] Genre: {info[1]}")
    print(f"[3] Restriction: {info[2]}")
    print(f"[4] Venue: Cinema {info[3]}")
    print(f"[5] Date and Time of Viewing: {info[4]}, {info[5]} - {info[6]}")
    print(f"[6] Price: P{info[7]}")
    print("[0] Go back")

    choice = input("Enter choice: ")

    if choice == "1":
        name = input("Enter new name: ")
        info[0] = name
    elif choice == "2":
        genre = input("Enter new genre: ")
        info[1] = genre
    elif choice == "3":
        restrict = input("Enter new restriction [G | PG | RPG | R18+]: ")
        info[2] = restrict
    elif choice == "4":
        cinema = input("Enter new cinema: ")
        info[3] = cinema
    elif choice == "5":
        print(f"[1] Date: {info[4]}")
        print(f"[2] Start time: {info[5]}")
        print(f"[3] End time: {info[6]}")

        edit = input("Choose detail to edit: ")

        if edit == "1":
            date = input("Enter new date [mm/dd/yy]: ")
            info[4] = date
        elif edit == "2":
            start = input("Enter new start time: [HH:MM (24)]: ")
            info[5] = start
        elif edit == "3":
            end = input("Enter new end time: [HH:MM (24)]: ")
            info[6] = end
        else:
            print("Invalid input")
    elif choice == "6":
        price = int(input("Enter new price: "))
        info[7] = price
    elif choice == "0":
        editMovie(movies)
    else:
        print("Invalid input")

    with open("movies.txt", "r") as f:
        lines = f.readlines()

    with open("movies.txt", "w") as f: 
        for i, line in enumerate(lines, 1):
            if i == 2:
                print(movies, file = f)
            else:
                f.writelines(line)

def editAllDetails(movies, movieID):
    name = input("Enter new Movie Name: ")
    genre = input("Enter new Genre: ")
    restrict = input("Enter new Movie Restriction [G | PG | RPG | R18+]: ")
    venue = input("Enter new Cinema Venue [1 | 2 | 3]: ")
    date = input("Enter new Date [mm/dd/yy]: ")
    startTime = input("Enter new start time: [HH:MM (24)]: ")
    endTime = input("Enter new end time: [HH:MM (24)]: ")
    price = int(input("Enter new price: "))

    movies[movieID] = [name, genre, restrict, venue, date, startTime, endTime, price]

    with open("movies.txt", "r") as f:
        lines = f.readlines()

    with open("movies.txt", "w") as f: 
        for i, line in enumerate(lines, 1):
            if i == 2:
                print(movies, file = f)
            else:
                f.writelines(line)

def deleteMovie(movies):
    moviesDel = [] # so i can catch the "Dictionary changed size during iteration" error

    print("[1] Delete a movie by ID")
    print("[2] Delete all movies in a cinema by day")
    print("[3] Delete all movies in all cinema by name")
    
    choice = input("Enter choice: ")

    if choice == "1":
        print("Movie List")
        for k, v in movies.items():
            print(k, "-", v[0])

        movieID = input("Enter Movie ID to delete [0 to cancel]: ")
        del movies[movieID]
    elif choice == "2":
        date = input("Enter date: ")
        cinema = input("Enter cinema: ")

        print(f"Movies at Cinema {cinema} on {date}")
        for k, v in movies.items():
            if cinema == v[3] and date == v[4]:
                print(f"{k} - {v[0]}")
                moviesDel.append(k)

        answer = input("Are you sure to delete this/these movie/s [y | n]: ")
        if answer == 'y':
            for k in list(moviesDel):
                if k in movies:
                    del movies[k]

        moviesDel = []
    elif choice == "3":
        name = input("Enter movie name: ")

        for k, v in movies.items():
            if name == v[0]:
                print(f"{k} - {v[0]}")
                moviesDel.append(k)

        answer = input("Are you sure to delete this/these movie/s [y | n]: ")
        if answer == 'y':
            for k in list(moviesDel):
                if k in movies:
                    del movies[k]
    else:
        print("Invalid input")

    with open("movies.txt", "r") as f:
        lines = f.readlines()

    with open("movies.txt", "w") as f: 
        for i, line in enumerate(lines, 1):
            if i == 2:
                print(movies, file = f)
            else:
                f.writelines(line)

def viewMovieAdmin():
    pass

# cashier
def viewMovieCashier():
    pass

def bookMovie():
    pass

movies = {}

with open("movies.txt") as f:
    data = f.readlines()

if data[0] != "0":
    movies = ast.literal_eval(data[1])

while True:
    printUser(movies)