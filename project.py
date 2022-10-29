from audioop import add
import PySimpleGUI as sg
from datetimerange import DateTimeRange
import ast

sg.theme('DarkGrey5')

def chooseUser():
    global user
    user = sg.Window(
        "Movie Theater Booking System", 
        [[sg.T("Select a user: ")], 
        [sg.Button("Admin", s=10), sg.Button("Cashier", s=10)]])

    while True:
        event, values = user.read()
        if event == sg.WIN_CLOSED:
            break
        else:
            user.close()
            if event == "Admin":
                adminMain()
            elif event == "Cashier":
                cashierMain()

    user.close()

def adminMain():
    adminMainLayout = [
                    [sg.T("Select an option:")],
                    [sg.Button("Add movie")],
                    [sg.Button("Edit movie")],
                    [sg.Button("Delete movie")],
                    [sg.Button("View movie")],
                    [sg.Button("Go to Users")],
                    [sg.Button("Exit")]
                    ]

    adminMain = sg.Window("Admin Main Menu", adminMainLayout, modal = True)

    while True:
        event, values = adminMain.read()

        if event == sg.WIN_CLOSED:
            break
        else:
            adminMain.close()
            if event == "Add movie":
                addMovie()
            elif event == "Edit movie":
                pass
            elif event == "Delete movie":
                pass
            elif event == "View movie":
                pass
            elif event == "Go to Users":
                chooseUser()
            elif event == "Exit":
                exit()

    adminMain.close()

def cashierMain():
    cashierMainLayout = [
                    [sg.T("Select an option:")],
                    [sg.Button("View movie")],
                    [sg.Button("Book movie")],
                    [sg.Button("Go to Users")],
                    [sg.Button("Exit")]
                    ]

    cashierMain = sg.Window("Cashier Main Menu", cashierMainLayout, modal = True)

    while True:
        event, values = cashierMain.read()

        if event == sg.WIN_CLOSED:
            break
        else:
            cashierMain.close()
            if event == "View movie":
                pass
            elif event == "Book movie":
                pass
            elif event == "Go to Users":
                chooseUser()
            elif event == "Exit":
                exit()

    cashierMain.close()

# Admin
def addMovie():
    addMovieLayout = [
                    [sg.T("Enter Movie name: "), sg.Input(key = "-NAME-", do_not_clear = True, size = (20,1))],
                    [sg.T("Enter Movie Genre: "), sg.Input(key = "-GENRE-", do_not_clear = True, size = (20,1))],
                    [sg.T("Choose Parental Rating: "), sg.Radio("G", "RESTRICT", key = "-G-", default = True), sg.Radio("PG", "RESTRICT", key = "-PG-"), sg.Radio("SPG", "RESTRICT", key = "-SPG-"), sg.Radio("R18", "RESTRICT", key = "-R18-")],
                    [sg.T("Choose Cinema Venue: "), sg.Radio("1", "CINEMA", key = "-1-", default = True), sg.Radio("2", "CINEMA", key = "-2-"), sg.Radio("3", "CINEMA", key = "-3-")],
                    [sg.T("Choose Date: "), sg.Input(key='-DATE-', size=(20,1)), sg.CalendarButton("Open Calendar", close_when_date_chosen=True,  target='-DATE-', format = "%m-%d-%y", location=(0,0), no_titlebar=False)],
                    [sg.T("Enter Start Time: "), sg.Input(key='-STARTHOUR-', size=(5,1)), sg.T(":"), sg.Input(key='-STARTMIN-', size=(5,1)), sg.Radio("AM", "START12H", key = "-STARTAM-", default = True), sg.Radio("PM", "START12H", key = "-STARTPM-")],
                    [sg.T("Enter End Time: "), sg.Input(key='-ENDHOUR-', size=(5,1)), sg.T(":"), sg.Input(key='-ENDMIN-', size=(5,1)), sg.Radio("AM", "END12H", key = "-ENDAM-", default = True), sg.Radio("PM", "END12H", key = "-ENDPM-")],
                    [sg.T("Enter Movie Price: "), sg.Input(key = "-PRICE-", do_not_clear = True, size = (20,1))],
                    [sg.Button("Add Movie"), sg.Button("Cancel")]
                    ]

    addMovie = sg.Window("Add Movie", addMovieLayout, modal = True)

    input_key_list = [key for key, value in addMovie.key_dict.items()
                    if isinstance(value, sg.Input)]


    while True:
        event, values = addMovie.read()

        if values["-G-"]:
            restrict = "G"
        elif values["-PG-"]:
            restrict = "PG"
        elif values["-SPG-"]:
            restrict = "SPG"
        else:
            restrict = "R18"

        if values["-1-"]:
            cinema = "1"
        elif values["-PG-"]:
            cinema = "2"
        else:
            cinema = "3"
        
        startTime = values["-STARTHOUR-"] + ":" + values["-STARTMIN-"]
        if values["-STARTAM-"]:
            startTime += "AM"
        else:
            startTime += "PM"

        endTime = values["-ENDHOUR-"] + ":" + values["-ENDMIN-"]
        if values["-ENDAM-"]:
            endTime += "AM"
        else:
            endTime += "PM"

        inConflict = False

        if event == sg.WIN_CLOSED:
            break
        else:
            if event == "Add Movie":
                for k, v in movies.items():
                    if v[3] == cinema and v[4] == values["-DATE-"] and (startTime in DateTimeRange(v[5], v[6]) or endTime in DateTimeRange(v[5], v[6])):
                        sg.Popup(f"This movie will be in conflict with {k} - {v[0]} [Cinema {v[3]}]: {v[4]} {v[5]} - {v[6]}.")
                        inConflict = True
                if all(map(str.strip, [values[key] for key in input_key_list])) and not inConflict:
                    addMovie.close()
                    addMovieInfo(restrict, cinema, startTime, endTime, values)
                    adminMain()
                elif not all(map(str.strip, [values[key] for key in input_key_list])):
                    sg.popup("Some inputs are missed!")

def addMovieInfo(restrict, cinema, startTime, endTime, values):
    with open("movies.txt", "r") as f:
        intMovieID = int(f.readline()) + 1

    movieID = str(intMovieID).zfill(4)

    movies[movieID] = [values["-NAME-"], values["-GENRE-"], restrict, cinema, values["-DATE-"], startTime, endTime, int(values["-PRICE-"])]
    booked[movieID] = []

    with open("movies.txt", "w") as f:
        f.write(str(intMovieID))
        print("\n", movies, file = f)

    with open("seats.txt", "w") as f: 
        print(seats, file = f)
        print(booked, file = f)

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

chooseUser()
exit()