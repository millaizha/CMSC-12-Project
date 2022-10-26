from datetime import datetime
from datetimerange import DateTimeRange
from colorama import Fore, Style
import ast

def printUser(movies, seats, booked):
    print("Select type of user: ")
    print("[1] Admin")
    print("[2] Cashier")
    print("[0] Exit")

    choice = input("Enter user: ")

    if choice == "1":
        adminMain(movies)
    elif choice == "2":
        cashierMain(seats, booked)
    elif choice == "0":
        print("Good bye")
        exit()
    else:
        print("Invalid input")

def adminMain(movies):
    while True:
        print("-" * 20 + "ADMIN MENU" + "-" * 20)
        print(f"Time: {datetime.strftime(datetime.now(), '%m/%d/%y %I:%M %p')}")

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
            viewMovieAdmin(movies)
        elif choice == "5":
            printUser(movies, seats, booked)
        elif choice == "0":
            print("Good bye")
            exit()
        else:
            print("Invalid input")


def cashierMain(seats, booked):
    while True:
        print("-" * 20 + "CASHIER MENU" + "-" * 20)
        print(f"Time: {datetime.strftime(datetime.now(), '%m/%d/%y %I:%M %p')}")

        print("[1] View Movies")
        print("[2] Book Movies")
        print("[3] Go back")
        print("[0] Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            viewMovieCashier()
        elif choice == "2":
            bookMovie(seats, booked)
        elif choice == "3":
            printUser(movies,seats, booked)
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
    date = str(datetime.strptime(input("Enter Date [mm/dd/yy]: "), '%m/%d/%y').date())
    startTime = str(datetime.strptime(input("Enter start time: [HH:MM AM/PM]: "), '%I:%M %p').time())
    endTime = str(datetime.strptime(input("Enter end time: [HH:MM AM/PM]: "), '%I:%M %p').time())
    for k, v in movies.items():
        if v[3] == venue and v[4] == date and (startTime in DateTimeRange(v[5], v[6]) or endTime in DateTimeRange(v[5], v[6])):
            print(f"This movie will be in conflict with {k} - {v[0]} [Cinema {v[3]}]: {datetime.strftime(datetime.strptime(v[4], '%Y-%m-%d'), '%m/%d/%y')} {datetime.strftime(datetime.strptime(v[5], '%H:%M:%S'), '%I:%M %p')} - {datetime.strftime(datetime.strptime(v[6], '%H:%M:%S'), '%I:%M %p')}.")
            adminMain(movies)
    price = int(input("Enter price: "))

    movies[MovieID] = [name, genre, restrict, venue, date, startTime, endTime, price]
    booked[MovieID] = []

    with open("movies.txt", "w") as f:
        f.write(str(intMovieID))
        print("\n", movies, file = f)

    with open("seats.txt", "w") as f: 
        print(seats, file = f)
        print(booked, file = f)

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
            date = str(datetime.strptime(input("Enter new date [mm/dd/yy]: "), '%m/%d/%y').date())
            info[4] = date
        elif edit == "2":
            start = str(datetime.strptime(input("Enter new start time: [HH:MM AM/PM]: "), '%I:%M %p').time())
            info[5] = start
        elif edit == "3":
            end = str(datetime.strptime(input("Enter new end time: [HH:MM AM/PM]: "), '%I:%M %p').time())
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
    date = str(datetime.strptime(input("Enter new Date [mm/dd/yy]: "), '%m/%d/%y').date())
    startTime = str(datetime.strptime(input("Enter new start time: [HH:MM AM/PM]: "), '%I:%M %p').time())
    endTime = str(datetime.strptime(input("Enter new end time: [HH:MM AM/PM]: "), '%I:%M %p').time())
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
        del booked[movieID]
    elif choice == "2":
        date = str(datetime.strptime(input("Enter date: "), '%m/%d/%y').date())
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
                    del booked[k]

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
                    del booked[k]

        moviesDel = []
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

    with open("seats.txt", "w") as f: 
        print(seats, file = f)
        print(booked, file = f)

def viewMovieAdmin(movies):
    print("[1] View all movies")
    print("[2] View all movies in a cinema by day")
    print("[3] View all details of a movie by id")
    print("[4] View all movie screening with a specific name")

    choice = input("Enter choice: ")

    if choice == "1":
        print("Movie list")
        for k, v in movies.items():
            print(f"{k} - {v[0]} - [Cinema {v[3]}] {datetime.strftime(datetime.strptime(v[4], '%Y-%m-%d'), '%m/%d/%Y')} {datetime.strftime(datetime.strptime(v[5], '%H:%M:%S'), '%I:%M %p')} - {datetime.strftime(datetime.strptime(v[6], '%H:%M:%S'), '%I:%M %p')}")
    elif choice == "2":
        date = str(datetime.strftime(datetime.strptime(input("Enter date: "), '%m/%d/%y'), '%Y-%m-%d'))
        cinema = input("Enter cinema: ")

        print(f"Movies at Cinema {cinema} on {date}")
        for k, v in movies.items():
            if v[3] == cinema and v[4] == date:
                print(f"{k} - {v[0]} [{datetime.strftime(datetime.strptime(v[5], '%H:%M:%S'), '%I:%M %p')} - {datetime.strftime(datetime.strptime(v[6], '%H:%M:%S'), '%I:%M %p')}]")
    elif choice == "3":
        print("Movie List")
        for k, v in movies.items():
            print(k, "-", v[0])

        movie = input("Enter movie ID: ")

        print(f"Movie {movie} Details:")
        print(f"Name: {movies[movie][0]}")
        print(f"Genre: {movies[movie][1]}")
        print(f"Restriction: {movies[movie][2]}")
        print(f"Venue: Cinema {movies[movie][3]}")
        print(f"Date and Time of Viewing: {datetime.strftime(datetime.strptime(movies[movie][4], '%Y-%m-%d'), '%m/%d/%y')} {datetime.strftime(datetime.strptime(movies[movie][5], '%H:%M:%S'), '%I:%M %p')} - {datetime.strftime(datetime.strptime(movies[movie][6], '%H:%M:%S'), '%I:%M %p')}")
        print(f"Price: P{movies[movie][7]}")
        print(f"Total Earnings from Booked Seats: P{movies[movie][7] * len(booked[movie])}")
    elif choice == "4":
        viewDict = {}
        name = input("Enter name: ")

        for k, v in movies.items():
            if name == v[0]:
                viewDict[k] = v

        viewDict = sorted(viewDict, key = lambda k: ([viewDict[k][4]], viewDict[k][5]))

        print(f"Movies named \"{name}\":")
        for i in viewDict:
            print(f"{i} - {movies[i][0]} [Cinema {movies[i][3]}] {datetime.strftime(datetime.strptime(movies[i][4], '%Y-%m-%d'), '%m/%d/%y')} {datetime.strftime(datetime.strptime(movies[i][5], '%H:%M:%S'), '%I:%M %p')} - {datetime.strftime(datetime.strptime(movies[i][6], '%H:%M:%S'), '%I:%M %p')}")
    else:
        print("Invalid Input")
        
# cashier
def viewMovieCashier(movies):
    print("[1] View all movies")
    print("[2] View movie by name")

    choice = input("Enter choice: ")

    if choice == "1":
        print("Movie list")
        for k, v in movies.items():
            print(f"{v[0]} - [Cinema {v[3]}] {datetime.strftime(datetime.strptime(v[4], '%Y-%m-%d'), '%m/%d/%Y')} {datetime.strftime(datetime.strptime(v[5], '%H:%M:%S'), '%I:%M %p')} - {datetime.strftime(datetime.strptime(v[6], '%H:%M:%S'), '%I:%M %p')}")
    elif choice == "2":
        viewDict = {}
        name = input("Enter name: ")

        for k, v in movies.items():
            if name == v[0]:
                viewDict[k] = v

        viewDict = sorted(viewDict, key = lambda k: ([viewDict[k][4]], viewDict[k][5]))

        print(f"Movies named \"{name}\":")
        for i in viewDict:
            print(f"{movies[i][0]} [Cinema {movies[i][3]}] {datetime.strftime(datetime.strptime(movies[i][4], '%Y-%m-%d'), '%m/%d/%y')} {datetime.strftime(datetime.strptime(movies[i][5], '%H:%M:%S'), '%I:%M %p')} - {datetime.strftime(datetime.strptime(movies[i][6], '%H:%M:%S'), '%I:%M %p')}")
    else:
        print("Invalid input")

def bookMovie(seats,booked):
    bookedSeats = []

    print("Movie list")
    for k, v in movies.items():
        print(f"{k} - {v[0]} - [Cinema {v[3]}] {datetime.strftime(datetime.strptime(v[4], '%Y-%m-%d'), '%m/%d/%Y')} {datetime.strftime(datetime.strptime(v[5], '%H:%M:%S'), '%I:%M %p')} - {datetime.strftime(datetime.strptime(v[6], '%H:%M:%S'), '%I:%M %p')}")

    movie = input("Select a movie ID: ")

    book = int(input("Enter number of seats to book: "))

    for i in range(book):
        if movies[movie][3] == "1":
            for j in range(len(seats) + 1):
                for k in seats:
                    if k[j] in booked[movie]:
                        print(Fore.RED + k[j], end=f" {Style.RESET_ALL}")
                    else:
                        print(k[j], end=" ")
                print()
        elif movies[movie][3] == "2":
            for j in range(len(seats)):
                for k in seats:
                    if k[j] in booked[movie]:
                        print(Fore.RED + k[j], end=f" {Style.RESET_ALL}")
                    else:
                        print(k[j], end=" ")
                print()
        elif movies[movie][3] == "3":
            for j in range(len(seats) - 1):
                for k in seats:
                    if k[j] in booked[movie]:
                        print(Fore.RED + k[j], end=f" {Style.RESET_ALL}")
                    else:
                        print(k[j], end=" ")
                print()

        while len(bookedSeats) < book:
            seat = input(f"Enter seat {i + 1}: ")
            if seat in booked[movie]:
                print("This seat is already taken!")
                continue
            else:
                booked[movie].append(seat)
                bookedSeats.append(seat)
            break

        with open("seats.txt", "w") as f: 
            print(seats, file = f)
            print(booked, file = f)

    printReceipt(bookedSeats, movie)

def printReceipt(book, movie):
    amountDue = movies[movie][7] * len(book)
    print(f"Your current amount due is {amountDue}.")
    
    code = input("Enter discount code [0 if none]: ")

    if code in discount:
        amountDue = (amountDue * (100 - discount[code])) / 100
    while True:
        cash = float(input("Enter cash: "))
        if cash < amountDue:
            print(f"Insufficient cash. Need {amountDue - cash} more.")
        else:
            break

    change = cash - amountDue

    print("-" * 20)
    print("Booking and Payment Details: ")
    print(f"Booking date\t\t: {datetime.strftime(datetime.now(), '%m/%d/%y %I:%M %p')}")
    print(f"Amount Due\t\t: {amountDue:.2f}")
    print(f"Cash\t\t\t: {cash:.2f}")
    print(f"Change\t\t\t: {change:.2f}")
    if code in discount:
        print(f"Discount\t\t: {discount[code]}%")

    print("-" * 20)
    print("Movie Details:")
    print(f"Movie\t\t\t: {movies[movie][0]}")
    print(f"Date and Time\t\t: {datetime.strftime(datetime.strptime(movies[movie][4], '%Y-%m-%d'), '%m/%d/%y')} {datetime.strftime(datetime.strptime(movies[movie][5], '%H:%M:%S'), '%I:%M %p')} - {datetime.strftime(datetime.strptime(movies[movie][6], '%H:%M:%S'), '%I:%M %p')}")
    print(f"Genre\t\t\t: {movies[movie][1]}")
    print(f"Parental Rating\t\t: {movies[movie][2]}")
    print(f"Cinema Number\t\t: Cinema {movies[movie][3]}")
    print(f"Number of tickets\t: {len(book)}")
    print("Seat Number/s\t\t:", *book)

movies = {}
seats = []
booked = {}
discount = {}

with open("movies.txt") as f:
    data = f.readlines()

if data[0] != "0":
    movies = ast.literal_eval(data[1])

with open("seats.txt") as f:
    data = f.readlines()

seats = ast.literal_eval(data[0])
booked = ast.literal_eval(data[1])

with open("discount.txt") as f:
    for line in f:
        (key, val) = line.split()
        discount[key] = int(val)

while True:
    printUser(movies, seats, booked)