import PySimpleGUI as sg
from datetime import datetime
from datetimerange import DateTimeRange
import ast

sg.theme('DarkGrey5')

def chooseUser():
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

    adminMain = sg.Window("Admin Main Menu", adminMainLayout, modal = True,  element_justification = "c")

    while True:
        event, values = adminMain.read()

        if event == sg.WIN_CLOSED:
            break
        else:
            adminMain.close()
            if event == "Add movie":
                addMovie()
            elif event == "Edit movie":
                editMovie()
            elif event == "Delete movie":
                deleteMovie()
            elif event == "View movie":
                viewMovieAdmin()
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
                    [sg.T("Choose Date: "), sg.Input(key='-DATE-', size=(20,1)), sg.CalendarButton("Open Calendar", close_when_date_chosen=True,  target='-DATE-', format = "%m-%d-%y", no_titlebar=False)],
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
        elif values["-R18-"]:
            restrict = "R18"

        if values["-1-"]:
            cinema = "1"
        elif values["-2-"]:
            cinema = "2"
        elif values["-3-"]:
            cinema = "3"
        
        startTime = values["-STARTHOUR-"].zfill(2) + ":" + values["-STARTMIN-"]
        if values["-STARTAM-"]:
            startTime += "AM"
        elif values["-STARTPM-"]:
            startTime += "PM"

        endTime = values["-ENDHOUR-"].zfill(2) + ":" + values["-ENDMIN-"]
        if values["-ENDAM-"]:
            endTime += "AM"
        elif values["-ENDPM-"]:
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
            elif event == "Cancel":
                addMovie.close()
                break
    adminMain()

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

def editMovie():
    movieList = [f"{k} - {v[0]}" for k, v in movies.items()]
    movieInfo = {}

    showMovieList = [
                    [sg.T("Select a Movie:")],
                    [sg.T("Search: "), sg.Input(size=(20, 1), enable_events=True, key='-SEARCH-')],
                    [sg.Listbox(movieList, size=(40, 10), enable_events = True, key='-MOVIE-')],
                    [sg.Button("Cancel")]
                    ]

    showMovieInfo = [
                    [sg.T("Movie Information:")],
                    [sg.Listbox(movieInfo, size=(50, 7), enable_events = True, key='-MOVIEINFO-')],
                    [sg.Button("Edit Movie Information")],
                    [sg.Button("Clear")]
                    ]
    editMovieLayout = [
                      [sg.Column(showMovieList, element_justification = "c"), sg.Column(showMovieInfo, element_justification="c")]
                      ]
    editMovie = sg.Window("Edit Movie", editMovieLayout)

    while True:
        event, values = editMovie.read()

        if event == sg.WIN_CLOSED:
            break

        if values['-SEARCH-'] != '':
            search = values['-SEARCH-']
            new_values = [x for x in movieList if search in x]
            editMovie['-MOVIE-'].update(new_values) 
        else:
            editMovie['-MOVIE-'].update(movieList)

        if event == '-MOVIE-' and len(values['-MOVIE-']):
            movieKey = str(values["-MOVIE-"])[2:6]
            movieInfo = [f"Movie ID: {movieKey}", f"Movie Name: {movies[movieKey][0]}", 
                        f"Movie Genre: {movies[movieKey][1]}", f"Parental Ratings: {movies[movieKey][2]}",
                        f"Cinema Room: {movies[movieKey][3]}", f"Date and Time of Viewing: {movies[movieKey][4]} {movies[movieKey][5]} - {movies[movieKey][6]}",
                        f"Price: P{movies[movieKey][7]}"]
            editMovie["-MOVIEINFO-"].update(movieInfo)

        if event == "Edit Movie Information" and bool(movieInfo):
            editMovieInfo(movieKey)
            editMovie['-MOVIEINFO-'].update([])
        elif event == "Clear":
            editMovie['-MOVIEINFO-'].update([])
        elif event == "Cancel":
            editMovie.close()
            break
    adminMain()

def editMovieInfo(movieKey):
    editMovieInfoLayout = [
                    [sg.T("Enter Movie name: "), sg.Input(movies[movieKey][0], key = "-NAME-", do_not_clear = True, size = (20,1))],
                    [sg.T("Enter Movie Genre: "), sg.Input(movies[movieKey][1], key = "-GENRE-", do_not_clear = True, size = (20,1))],
                    [sg.T("Choose Parental Rating: "), sg.Radio("G", "RESTRICT", key = "-G-", default = True), sg.Radio("PG", "RESTRICT", key = "-PG-"), sg.Radio("SPG", "RESTRICT", key = "-SPG-"), sg.Radio("R18", "RESTRICT", key = "-R18-")],
                    [sg.T("Choose Cinema Venue: "), sg.Radio("1", "CINEMA", key = "-1-", default=True), sg.Radio("2", "CINEMA", key = "-2-"), sg.Radio("3", "CINEMA", key = "-3-"              )],
                    [sg.T("Choose Date: "), sg.Input(movies[movieKey][4], key='-DATE-', size=(20,1)), sg.CalendarButton("Open Calendar", close_when_date_chosen=True,  target='-DATE-', format = "%m-%d-%y", location=(0,0), no_titlebar=False)],
                    [sg.T("Enter Start Time: "), sg.Input(movies[movieKey][5][:2], key='-STARTHOUR-', size=(5,1)), sg.T(":"), sg.Input(movies[movieKey][5][3:5], key='-STARTMIN-', size=(5,1)), sg.Radio("AM", "START12H", key = "-STARTAM-", default = True), sg.Radio("PM", "START12H", key = "-STARTPM-")],
                    [sg.T("Enter End Time: "), sg.Input(movies[movieKey][6][:2], key='-ENDHOUR-', size=(5,1)), sg.T(":"), sg.Input(movies[movieKey][6][3:5], key='-ENDMIN-', size=(5,1)), sg.Radio("AM", "END12H", key = "-ENDAM-", default = True), sg.Radio("PM", "END12H", key = "-ENDPM-")],
                    [sg.T("Enter Movie Price: "), sg.Input(movies[movieKey][7], key = "-PRICE-", do_not_clear = True, size = (20,1))],
                    [sg.Button("Finish Editing Movie"), sg.Button("Cancel")]
                    ]

    editMovieInfo = sg.Window("Edit Movie Info", editMovieInfoLayout, finalize = True)

    input_key_list = [key for key, value in editMovieInfo.key_dict.items()
                    if isinstance(value, sg.Input)]

    while True:        
        if movies[movieKey][2] == "PG":
            editMovieInfo.Element("-PG-").update(value = True)
        elif movies[movieKey][2] == "SPG":
            editMovieInfo.Element("-SPG-").update(value = True)
        elif movies[movieKey][2] == "R18":
            editMovieInfo.Element("-R18-").update(value = True)

        if movies[movieKey][3] == "2":
            editMovieInfo.Element("-2-").update(value = True)
        elif movies[movieKey][3] == "3":
            editMovieInfo.Element("-3-").update(value = True)

        if movies[movieKey][5][-2:] == "PM":
            editMovieInfo.Element("-STARTPM-").update(value = True)
        if movies[movieKey][6][-2:] == "PM":
            editMovieInfo.Element("-ENDPM-").update(value = True)

        event, values = editMovieInfo.read()

        inConflict = False

        if event == sg.WIN_CLOSED:
            break
        else:
            if values["-G-"]:
                restrict = "G"
            elif values["-PG-"]:
                restrict = "PG"
            elif values["-SPG-"]:
                restrict = "SPG"
            elif values["-R18-"]:
                restrict = "R18"

            if values["-1-"]:
                cinema = "1"
            elif values["-2-"]:
                cinema = "2"
            elif values["-3-"]:
                cinema = "3"
        
            startTime = values["-STARTHOUR-"] + ":" + values["-STARTMIN-"]
            if values["-STARTAM-"]:
                startTime += "AM"
            elif values["-STARTPM-"]:
                startTime += "PM"

            endTime = values["-ENDHOUR-"] + ":" + values["-ENDMIN-"]
            if values["-ENDAM-"]:
                endTime += "AM"
            elif values["-ENDPM-"]:
                endTime += "PM"
                
            if event == "Finish Editing Movie":
                for k, v in movies.items():
                    if k != movieKey and v[3] == cinema and v[4] == values["-DATE-"] and (
                        startTime in DateTimeRange(v[5], v[6]) or endTime in DateTimeRange(v[5], v[6])):
                        sg.Popup(f"This movie will be in conflict with {k} - {v[0]} [Cinema {v[3]}]: {v[4]} {v[5]} - {v[6]}.")
                        inConflict = True
                if all(map(str.strip, [values[key] for key in input_key_list])) and not inConflict:
                    saveEditInfo(restrict, cinema, startTime, endTime, values, movieKey)
                elif not all(map(str.strip, [values[key] for key in input_key_list])):
                    sg.popup("Some inputs are missed!")
                editMovieInfo.close()
            elif event == "Cancel":
                editMovieInfo.close()
                break

def saveEditInfo(restrict, cinema, startTime, endTime, values, movieKey):
    movies[movieKey] = [values["-NAME-"], values["-GENRE-"], restrict, cinema, values["-DATE-"], startTime, endTime, int(values["-PRICE-"])]

    updateFiles()

def deleteMovie():
    deleteMovieLayout = [
                        [sg.Button("Delete a movie by ID")],
                        [sg.Button("Delete all movies in a Cinema by Day")],
                        [sg.Button("Delete all movies in all cinema by name")],
                        [sg.Button("Go Back")],
                        ]

    deleteMovie = sg.Window("Delete Movie", deleteMovieLayout, element_justification = "c")

    while True:
        event, values = deleteMovie.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == "Delete a movie by ID":
            deleteMovieByID()
        elif event == "Delete all movies in a Cinema by Day":
            deleteMovieByDay()
        elif event == "Delete all movies in all cinema by name":
            deleteMovieByName()
        elif event == "Go Back":
            pass
        
        deleteMovie.close()
        adminMain()

def deleteMovieByID():
    movieList = [f"{k} - {v[0]}" for k, v in movies.items()]
    movieInfo = {}

    showMovieList = [
                    [sg.T("Select a Movie:")],
                    [sg.T("Search: "), sg.Input(size=(20, 1), enable_events=True, key='-SEARCH-')],
                    [sg.Listbox(movieList, size=(40, 10), enable_events = True, key='-MOVIE-')],
                    [sg.Button("Cancel")]
                    ]

    showMovieInfo = [
                    [sg.T("Movie Information:")],
                    [sg.Listbox(movieInfo, size=(50, 7), enable_events = True, key='-MOVIEINFO-')],
                    [sg.Button("Delete Movie")]
                    ]

    deleteMovieByIDLayout = [
                      [sg.Column(showMovieList, element_justification = "c"), sg.Column(showMovieInfo, element_justification="c")]
                      ]
    deleteMovieByID = sg.Window("Delete Movie", deleteMovieByIDLayout)

    while True:
        event, values = deleteMovieByID.read()

        if event == sg.WIN_CLOSED:
            break

        if values['-SEARCH-'] != '':
            search = values['-SEARCH-']
            new_values = [x for x in movieList if search in x]
            deleteMovieByID['-MOVIE-'].update(new_values) 
        else:
            deleteMovieByID['-MOVIE-'].update(movieList)

        if event == '-MOVIE-' and len(values['-MOVIE-']):
            movieKey = str(values["-MOVIE-"])[2:6]
            movieInfo = [f"Movie ID: {movieKey}", f"Movie Name: {movies[movieKey][0]}", 
                        f"Movie Genre: {movies[movieKey][1]}", f"Parental Ratings: {movies[movieKey][2]}",
                        f"Cinema Room: {movies[movieKey][3]}", f"Date and Time of Viewing: {movies[movieKey][4]} {movies[movieKey][5]} - {movies[movieKey][6]}",
                        f"Price: P{movies[movieKey][7]}"]
            deleteMovieByID["-MOVIEINFO-"].update(movieInfo)

        if event == "Delete Movie" and bool(movieInfo):
            answer = sg.popup_yes_no(f"Are you sure to delete {movieKey} - {movies[movieKey][0]}?")
            if answer == "Yes":
                del movies[movieKey]
                del booked[movieKey]
                deleteMovieByID['-MOVIEINFO-'].update([])
        elif event == "Cancel":
            deleteMovieByID.close()
            break

        movieList = [f"{k} - {v[0]}" for k, v in movies.items()]
        deleteMovieByID['-MOVIE-'].update(movieList)

        updateFiles()

    deleteMovie()

def deleteMovieByDay():
    moviesDel = []

    deleteMovieByDayLayout = [
                             [sg.T("Select a Date: "), sg.Input(key='-DATE-', size=(20,1)), sg.CalendarButton("Open Calendar", close_when_date_chosen=True,  target='-DATE-', format = "%m-%d-%y", no_titlebar=False)],
                             [sg.T("Select a  Cinema Venue: "), sg.Radio("1", "CINEMA", key = "-1-", default = True), sg.Radio("2", "CINEMA", key = "-2-"), sg.Radio("3", "CINEMA", key = "-3-")],
                             [sg.Button("Search Movies")],
                             [sg.Button("Cancel")]
                             ]

    deleteMovieByDay = sg.Window("Delete Movie", deleteMovieByDayLayout, modal = True, element_justification = "c")

    input_key_list = [key for key, value in deleteMovieByDay.key_dict.items()
                    if isinstance(value, sg.Input)]

    while True:
        event, values = deleteMovieByDay.read()
        cinema = "1"
        if values["-2-"]:
            cinema = "2"
        elif values["-3-"]:
            cinema = "3"

        date = values["-DATE-"]

        if event == sg.WIN_CLOSED:
            break
        if event == "Search Movies":
            for k, v in movies.items():
                if cinema == v[3] and date == v[4]:
                    moviesDel.append(k)

            if all(map(str.strip, [values[key] for key in input_key_list])):
                if len(moviesDel) == 0:
                    sg.popup(f"There are no movies on {date} in Cinema {cinema}")
                else:
                    answer = deletePopup(moviesDel)
                    if answer == "Yes":
                        for k in moviesDel:
                            if k in movies:
                                del movies[k]
                                del booked[k]
                        updateFiles()
                    deleteMovieByDay.close()
                    break
            else:
                sg.popup("Some inputs are missed!")   
        elif event == "Cancel":
            deleteMovieByDay.close()
            break         

def deleteMovieByName():
    moviesDel = []

    deleteMovieByNameLayout = [
                              [sg.T("Search movie name to delete:")],
                              [sg.Input(key = "-NAME-", do_not_clear = True, size = (20,1))],
                              [sg.Button("Search")],
                              [sg.Button("Cancel")]
                              ]

    deleteMovieByName = sg.Window("Delete movie", deleteMovieByNameLayout, element_justification = "c")

    while True:
        event, values = deleteMovieByName.read()

        name = values["-NAME-"]

        if event == sg.WIN_CLOSED:
            deleteMovieByName.close()
            break
        if event == "Search" and name != "":
            for k, v in movies.items():
                if values["-NAME-"] == v[0]:
                    moviesDel.append(k)
            if len(moviesDel) == 0:
                sg.popup(f"There is no movie named {name}")
            else:
                answer = deletePopup(moviesDel)
                if answer == "Yes":
                    for k in moviesDel:
                        if k in movies:
                            del movies[k]
                            del booked[k]
                    updateFiles()
                deleteMovieByName.close()
                break
        elif event == "Cancel":
            deleteMovieByName.close()

def deletePopup(data):
    layout =[
            [sg.T("Are you sure to delete the following movie/s?")],
            [[sg.T(f"{k} - {movies[k][0]}")] for k in data],
            [sg.Button("Yes"), sg.Button("No")]
            ]
    
    window = sg.Window("Delete movie", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "No":
            break
        else:
            window.close()
            return "Yes"

def viewMovieAdmin():
    viewMovieAdminLayout = [
                           [sg.Button("View all movies")],
                           [sg.Button("View all movies in a cinema by day")],
                           [sg.Button("View details of a movie")],
                           [sg.Button("View all movie screening by name")],
                           [sg.Button("Go back")]
                           ]

    viewMovieAdmin = sg.Window("View Movie", viewMovieAdminLayout, element_justification = "c")

    while True:
        event, values = viewMovieAdmin.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "View all movies":
            viewAllMoviesAdmin()
        elif event == "View all movies in a cinema by day":
            viewMovieInCinema()
        elif event == "View details of a movie":
            viewMovieDetails()
        elif event == "View all movie screening by name":
            viewMovieByName()
        elif event == "Go back":
            viewMovieAdmin.close()
            adminMain()

def viewAllMoviesAdmin():
    movieList = [f"{k} - {v[0]}" for k, v in movies.items()]

    showMovieList = [
                    [sg.T("Movie List:")],
                    [sg.Listbox(movieList, size=(40, 10), enable_events = True, key='-MOVIE-')],
                    [sg.Button("Go back")]
                    ]

    viewAllMoviesAdmin = sg.Window("View Movies", showMovieList, element_justification = "c")

    while True:
        event, values = viewAllMoviesAdmin.read()

        if event == sg.WIN_CLOSED:
            break
        if event == "Go back":
            viewAllMoviesAdmin.close()

def viewMovieInCinema():
    movieList = []

    searchMovie = [
                  [sg.T("Select a date:"), sg.Input(key='-DATE-', size=(20,1)), sg.CalendarButton("Open Calendar", close_when_date_chosen=True,  target='-DATE-', format = "%m-%d-%y", no_titlebar=False)],
                  [sg.T("Select Cinema:"), sg.Radio("1", "CINEMA", key = "-1-", default = True), sg.Radio("2", "CINEMA", key = "-2-"), sg.Radio("3", "CINEMA", key = "-3-")],
                  [sg.Button("Search")],
                  [sg.Button("Go back")]
                  ]

    showMovieList = [
                    [sg.T("Movie Search Results")],
                    [sg.Listbox(movieList, size=(50, 7), enable_events = True, key='-MOVIELIST-')],
                    [sg.Button("Clear")]
                    ]
    
    viewMovieInCinemaLayout = [
                              [sg.Column(searchMovie, element_justification = "c"), sg.Column(showMovieList, element_justification = "c")]
                              ]

    viewMovieInCinema = sg.Window("View Movies", viewMovieInCinemaLayout)

    while True:
        event, values = viewMovieInCinema.read()

        if values["-1-"]:
            cinema = "1"
        elif values["-2-"]:
            cinema = "2"
        elif values["-3-"]:
            cinema = "3"

        date = values["-DATE-"]

        if event == sg.WIN_CLOSED:
            break

        if event == "Search":
            viewMovieInCinema["-MOVIELIST-"].update([])
            movieList = []

            for k, v in movies.items():
                if v[3] == cinema and v[4] == date:
                    movieList.append(f"{k} - {v[0]}")

            if len(movieList) == 0:
                sg.popup(f"There are no movies on {date} at Cinema {cinema}")
            else:
                viewMovieInCinema["-MOVIELIST-"].update(movieList)
        elif event == "Clear":
            viewMovieInCinema["-MOVIELIST-"].update([])
            movieList = []
        elif event == "Go back":
            viewMovieInCinema.close()
            break

def viewMovieDetails():
    movieList = [f"{k} - {v[0]}" for k, v in movies.items()]
    movieInfo = {}

    showMovieList = [
                    [sg.T("Select a Movie:")],
                    [sg.T("Search: "), sg.Input(size=(20, 1), enable_events=True, key='-SEARCH-')],
                    [sg.Listbox(movieList, size=(40, 10), enable_events = True, key='-MOVIE-')],
                    [sg.Button("Cancel")]
                    ]

    showMovieInfo = [
                    [sg.T("Movie Information:")],
                    [sg.Listbox(movieInfo, size=(50, 8), enable_events = True, key='-MOVIEINFO-')],
                    [sg.Button("Clear")]
                    ]
    viewMovieDetailsLayout = [
                      [sg.Column(showMovieList, element_justification = "c"), sg.Column(showMovieInfo, element_justification="c")]
                      ]
    viewMovieDetails = sg.Window("View Movie", viewMovieDetailsLayout)

    while True:
        event, values = viewMovieDetails.read()

        if event == sg.WIN_CLOSED:
            break

        if values['-SEARCH-'] != '':
            search = values['-SEARCH-']
            new_values = [x for x in movieList if search in x]
            viewMovieDetails['-MOVIE-'].update(new_values) 
        else:
            viewMovieDetails['-MOVIE-'].update(movieList)

        if event == '-MOVIE-' and len(values['-MOVIE-']):
            movieKey = str(values["-MOVIE-"])[2:6]
            movieInfo = [f"Movie ID: {movieKey}", f"Movie Name: {movies[movieKey][0]}", 
                        f"Movie Genre: {movies[movieKey][1]}", f"Parental Ratings: {movies[movieKey][2]}",
                        f"Cinema Room: {movies[movieKey][3]}", f"Date and Time of Viewing: {movies[movieKey][4]} {movies[movieKey][5]} - {movies[movieKey][6]}",
                        f"Price: P{movies[movieKey][7]}", f"Total Earnings from Booked Seats: P{movies[movieKey][7] * len(booked[movieKey])}"]
            viewMovieDetails["-MOVIEINFO-"].update(movieInfo)

        if event == "Clear":
            viewMovieDetails['-MOVIEINFO-'].update([])
        elif event == "Cancel":
            viewMovieDetails.close()

def viewMovieByName():
    viewDict = {}
    movieList = []

    searchMovie = [
                  [sg.T("Search a Movie:"), sg.Input(key='-NAME-', size=(20,1))],
                  [sg.Button("Search")],
                  [sg.Button("Go back")]
                  ]

    showMovieList = [
                    [sg.T("Movie Search Results")],
                    [sg.Listbox(movieList, size=(50, 7), enable_events = True, key='-MOVIELIST-')],
                    [sg.Button("Clear")]
                    ]
    
    viewMovieByNameLayout = [
                              [sg.Column(searchMovie, element_justification = "c"), sg.Column(showMovieList, element_justification = "c")]
                              ]

    viewMovieByName = sg.Window("View Movies", viewMovieByNameLayout)

    while True:
        event, values = viewMovieByName.read()

        name = values["-NAME-"]

        if event == sg.WIN_CLOSED:
            break

        if event == "Search":
            for k, v in movies.items():
                if name == v[0]:
                    viewDict[k] = v

            viewDict = sorted(viewDict, key = lambda k: ([datetime.strptime((viewDict[k][4]), '%m-%d-%y').date()], [datetime.strptime((viewDict[k][5]), '%I:%M%p').time()]))
            movieList = [f"{k} - {movies[k][0]} [Cinema {movies[k][3]}] {movies[k][4]} {movies[k][5]} - {movies[k][6]}" for k in viewDict]

            if len(viewDict) == 0:
                sg.popup(f"There is no movie named {name}")
            else:
                viewMovieByName["-MOVIELIST-"].update(movieList)

            viewDict = {}
            movieList = []
        
        elif event == "Clear":
            viewMovieByName["-MOVIELIST-"].update([])

        elif event == "Go back":
            viewMovieByName.close()
            break

def updateFiles():
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